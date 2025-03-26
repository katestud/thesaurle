#!/bin/bash
set -e

# Check if snapshot exists
if [ -f /usr/lib/memgraph/snapshot ]; then
    echo "Snapshot found, it will be loaded on startup"
    # Move snapshot to the correct location for auto-loading
    cp /usr/lib/memgraph/snapshot /var/lib/memgraph/snapshot
else
    echo "No snapshot found, starting with empty database"
fi

# Start Memgraph
exec /usr/lib/memgraph/memgraph "$@"
