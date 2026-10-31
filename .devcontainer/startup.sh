#!/usr/bin/env bash
set -euo pipefail

# The multi-device sandbox is intentionally lightweight. The repository's
# full AutoGen/.NET development setup is opt-in so a Codespace can start
# without downloading the entire workspace's dependency graph.

if [[ "${SOPHIA_FULL_DEV_SETUP:-0}" == "1" ]]; then
  echo "Running the full repository development setup..."
  dotnet workload update
  dotnet dev-certs https --trust

  pushd python >/dev/null
  if ! command -v uv >/dev/null 2>&1; then
    pip install uv
  fi
  uv sync
  popd >/dev/null
else
  echo "Lightweight Sophia sandbox setup complete."
  echo "Docker availability will be checked in the Codespace terminal."
  echo "Set SOPHIA_FULL_DEV_SETUP=1 to opt into the full AutoGen/.NET setup."
fi
