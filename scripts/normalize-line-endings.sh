#!/bin/bash
set -euo pipefail

# Normalize line endings to LF for shell scripts in the repository.
# Prefer dos2unix if available, otherwise use sed.

if command -v dos2unix >/dev/null 2>&1; then
  echo "Using dos2unix to normalize .sh files..."
  find . -type f -name '*.sh' -print0 | xargs -0 dos2unix || true
else
  echo "dos2unix not found; using sed fallback to normalize .sh files..."
  find . -type f -name '*.sh' -print0 | xargs -0 sed -i 's/\r$//' || true
fi

echo "Line ending normalization complete."
