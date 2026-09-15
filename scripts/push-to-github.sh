#!/usr/bin/env bash
# Push main (and optional branches) to GitHub using GITHUB_TOKEN from the environment.
set -euo pipefail

GITHUB_REPO="${GITHUB_REPO:-https://github.com/sakshamgoyal06/magnus-ai.git}"

if [[ -z "${GITHUB_TOKEN:-}" ]]; then
  echo "GITHUB_TOKEN is not set. Add it as a Cloud Agent secret, then re-run this script." >&2
  exit 1
fi

AUTH_URL="https://x-access-token:${GITHUB_TOKEN}@github.com/sakshamgoyal06/magnus-ai.git"

git remote get-url github &>/dev/null || git remote add github "$GITHUB_REPO"

echo "Pushing main to GitHub..."
git push "$AUTH_URL" main:main

if git show-ref --verify --quiet refs/heads/cursor/day1-foundation-a615; then
  echo "Pushing cursor/day1-foundation-a615..."
  git push "$AUTH_URL" cursor/day1-foundation-a615:cursor/day1-foundation-a615
fi

echo "Done. GitHub: https://github.com/sakshamgoyal06/magnus-ai"
