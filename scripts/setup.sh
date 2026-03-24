#!/bin/bash
set -e

VENV_DIR="${CLAUDE_PLUGIN_DATA}/venv"
REQ_FILE="${CLAUDE_PLUGIN_ROOT}/requirements.txt"
REQ_HASH_FILE="${CLAUDE_PLUGIN_DATA}/requirements.hash"

# Compute hash of requirements.txt
CURRENT_HASH=$(shasum -a 256 "$REQ_FILE" | cut -d ' ' -f 1)
STORED_HASH=""
if [ -f "$REQ_HASH_FILE" ]; then
    STORED_HASH=$(cat "$REQ_HASH_FILE")
fi

# Only install if requirements changed or venv missing
if [ "$CURRENT_HASH" != "$STORED_HASH" ] || [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    "$VENV_DIR/bin/pip" install --quiet --upgrade pip
    "$VENV_DIR/bin/pip" install --quiet -r "$REQ_FILE"
    echo "$CURRENT_HASH" > "$REQ_HASH_FILE"
fi
