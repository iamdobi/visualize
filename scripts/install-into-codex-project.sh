#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  scripts/install-into-codex-project.sh <target-project> [plugin-git-url-or-path]

Examples:
  scripts/install-into-codex-project.sh ~/code/my-app
  scripts/install-into-codex-project.sh ~/code/my-app https://github.com/careerhackeralex/visualize.git

What it does:
  1. Installs this repo into <target-project>/plugins/visualize
  2. Creates or updates <target-project>/.agents/plugins/marketplace.json
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" || $# -lt 1 || $# -gt 2 ]]; then
  usage
  exit $([[ $# -lt 1 || $# -gt 2 ]] && echo 1 || echo 0)
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_SOURCE="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [[ ! -d "$1" ]]; then
  echo "Target project does not exist: $1" >&2
  exit 1
fi

TARGET_PROJECT="$(cd "$1" && pwd)"
PLUGIN_SOURCE="${2:-$DEFAULT_SOURCE}"
PLUGIN_DIR="${TARGET_PROJECT}/plugins/visualize"
MARKETPLACE_PATH="${TARGET_PROJECT}/.agents/plugins/marketplace.json"

if [[ -e "${PLUGIN_DIR}" ]]; then
  echo "Plugin destination already exists: ${PLUGIN_DIR}" >&2
  exit 1
fi

mkdir -p "${TARGET_PROJECT}/plugins"

if [[ -d "${PLUGIN_SOURCE}" ]]; then
  mkdir -p "${PLUGIN_DIR}"
  rsync -a --exclude '.git' --exclude '.gitmodules' "${PLUGIN_SOURCE}/" "${PLUGIN_DIR}/"
elif git -C "${TARGET_PROJECT}" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git -C "${TARGET_PROJECT}" submodule add "${PLUGIN_SOURCE}" "plugins/visualize"
else
  git clone "${PLUGIN_SOURCE}" "${PLUGIN_DIR}"
fi

python3 - "${MARKETPLACE_PATH}" <<'PY'
import json
import sys
from pathlib import Path

marketplace_path = Path(sys.argv[1])
entry = {
    "name": "visualize",
    "source": {
        "source": "local",
        "path": "./plugins/visualize",
    },
    "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL",
    },
    "category": "Productivity",
}

if marketplace_path.exists():
    payload = json.loads(marketplace_path.read_text())
else:
    payload = {
        "name": "local-plugins",
        "interface": {
            "displayName": "Local Plugins",
        },
        "plugins": [],
    }

plugins = payload.setdefault("plugins", [])
replaced = False
for index, existing in enumerate(plugins):
    if isinstance(existing, dict) and existing.get("name") == "visualize":
        plugins[index] = entry
        replaced = True
        break

if not replaced:
    plugins.append(entry)

marketplace_path.parent.mkdir(parents=True, exist_ok=True)
marketplace_path.write_text(json.dumps(payload, indent=2) + "\n")
PY

echo "Installed Visualize into ${PLUGIN_DIR}"
echo "Updated marketplace: ${MARKETPLACE_PATH}"
echo
echo "Next steps:"
echo "  1. Commit the new plugin directory and marketplace file in ${TARGET_PROJECT}"
echo "  2. Open the target project in Codex"
