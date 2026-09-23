#!/usr/bin/env bash
set -euo pipefail

REPO_NAME="${1:-agentic-gov-mission-copilot}"
VISIBILITY="${2:-public}"

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI (gh) is required: https://cli.github.com/"
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "Authenticate first with: gh auth login"
  exit 1
fi

if [[ "$VISIBILITY" != "public" && "$VISIBILITY" != "private" ]]; then
  echo "Visibility must be public or private"
  exit 1
fi

gh repo create "$REPO_NAME" --"$VISIBILITY" --source=. --remote=origin --push
