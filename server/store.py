"""LanceDB vector store abstraction."""

from pathlib import Path

import lancedb
import pyarrow as pa

SCHEMA = pa.schema([
    pa.field("id", pa.string()),
    pa.field("text", pa.string()),
    pa.field("source_file", pa.string()),
    pa.field("file_name", pa.string()),
    pa.field("file_type", pa.string()),
    pa.field("folder_path", pa.string()),
    pa.field("chunk_index", pa.int32()),
    pa.field("content_hash", pa.string()),
    pa.field("vector", pa.list_(pa.float32(), 384)),
])

TABLE_NAME = "chunks"


class VectorStore:
    def __init__(self, db_path: str):
        self._db_path = db_path
        self._db = lancedb.connect(db_path)
        self._table = None

    def _get_table(self):
        if self._table is None:
            try:
                self._table = self._db.open_table(TABLE_NAME)
            except Exception:
                return None
        return self._table

    def _ensure_table(self):
        table = self._get_table()
        if table is None:
            self._table = self._db.create_table(TABLE_NAME, schema=SCHEMA)
        return self._table

    def add_chunks(self, chunks: list[dict]) -> None:
        table = self._ensure_table()
        rows = []
        for c in chunks:
            rows.append({
                "id": c["id"],
                "text": c["text"],
                "source_file": c["source_file"],
                "file_name": c["file_name"],
                "file_type": c["file_type"],
                "folder_path": c["folder_path"],
                "chunk_index": c["chunk_index"],
                "content_hash": c["content_hash"],
                "vector": c["vector"],
            })
        table.add(rows)

    def count_chunks(self) -> int:
        table = self._get_table()
        if table is None:
            return 0
        return table.count_rows()

    def get_file_hash(self, source_file: str) -> str | None:
        table = self._get_table()
        if table is None:
            return None
        results = (
            table.search()
            .where(f"source_file = '{source_file}'", prefilter=True)
            .select(["content_hash"])
            .limit(1)
            .to_list()
        )
        if results:
            return results[0]["content_hash"]
        return None

    def delete_by_file(self, source_file: str) -> None:
        table = self._get_table()
        if table is None:
            return
        table.delete(f"source_file = '{source_file}'")

    def get_all_files(self) -> list[str]:
        table = self._get_table()
        if table is None:
            return []
        arrow_table = table.to_arrow().select(["source_file"])
        return list(set(arrow_table.column("source_file").to_pylist()))

    def vector_search(
        self,
        query_vector: list[float],
        top_k: int = 10,
        folder_path: str | None = None,
        file_type: str | None = None,
    ) -> list[dict]:
        table = self._get_table()
        if table is None:
            return []
        if table.count_rows() == 0:
            return []

        query = table.search(query_vector).metric("cosine").limit(top_k)

        where_clauses = []
        if folder_path:
            where_clauses.append(f"folder_path = '{folder_path}'")
        if file_type:
            where_clauses.append(f"file_type = '{file_type}'")
        if where_clauses:
            query = query.where(" AND ".join(where_clauses), prefilter=True)

        results = query.to_list()
        return [
            {
                "text": r["text"],
                "source_file": r["source_file"],
                "file_name": r["file_name"],
                "file_type": r["file_type"],
                "folder_path": r["folder_path"],
                "chunk_index": r["chunk_index"],
                "score": r.get("_distance", 0.0),
            }
            for r in results
        ]
