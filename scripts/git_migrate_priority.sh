#!/usr/bin/env bash
#
# Migrate the priority projects into private GitHub repos under the
# kevin-sotka org: Train Lore, The Gridiron Gazette, and SodClaw itself
# (the orchestrator). Run this ON YOUR MAC (not in Cowork) so it uses
# your real filesystem and your GitHub credentials.
# Already-migrated repos are skipped automatically, so re-running is safe.
#
#   cd ~/Meatbag_Labs && bash SodClaw/scripts/git_migrate_priority.sh
#
# Safe to re-run: it skips a repo that already has a .git directory.
# Requires git. Uses the GitHub CLI (gh) if installed; otherwise prints
# the manual create-and-push steps.

set -euo pipefail

ROOT="$HOME/Meatbag_Labs"
ORG="kevin-sotka"
AUTHOR_NAME="Kevin Sotka"
AUTHOR_EMAIL="kevinsotka@gmail.com"

# folder|repo-name|commit message
PROJECTS=(
  "train_lore|train_lore|Initial commit: Train Lore — PNW Railroad blog posts, images, topic list"
  "thegridirongazette|thegridirongazette|Initial commit: The Gridiron Gazette — landing page, news fetcher, mock draft (DB creds excluded)"
  "SodClaw|SodClaw|Initial commit: SodClaw orchestrator — CLAUDE.md, portfolio.json, dashboard, skills, workflows, profile"
)

have_gh() { command -v gh >/dev/null 2>&1; }

for entry in "${PROJECTS[@]}"; do
  IFS='|' read -r folder repo msg <<< "$entry"
  dir="$ROOT/$folder"
  echo ""
  echo "=================================================================="
  echo "  $folder  ->  github.com/$ORG/$repo  (private)"
  echo "=================================================================="

  if [ ! -d "$dir" ]; then
    echo "  SKIP: $dir not found."
    continue
  fi
  cd "$dir"

  if [ -d ".git" ]; then
    echo "  Already a git repo — skipping init/commit. (Push manually if needed.)"
    continue
  fi

  if [ ! -f ".gitignore" ]; then
    echo "  WARNING: no .gitignore in $folder. Aborting this one to be safe."
    continue
  fi

  git init -q
  git branch -M main
  git config user.name  "$AUTHOR_NAME"
  git config user.email "$AUTHOR_EMAIL"
  git add -A

  # --- SAFETY NET: never let the credential file get committed ---
  if git ls-files --cached | grep -q "signup_waitlist.php"; then
    echo "  !! ABORT: signup_waitlist.php is staged — it holds the live DB password."
    echo "  !! Check $folder/.gitignore. Nothing was committed."
    rm -rf .git
    continue
  fi

  git commit -q -m "$msg"
  echo "  Committed. Tracked files:"
  git ls-files | sed 's/^/    /'

  if have_gh; then
    echo "  Creating private repo and pushing via gh..."
    gh repo create "$ORG/$repo" --private --source=. --remote=origin --push
    echo "  DONE -> https://github.com/$ORG/$repo"
  else
    echo ""
    echo "  gh CLI not found. Finish manually:"
    echo "    1) Create an EMPTY private repo at: https://github.com/organizations/$ORG/repositories/new"
    echo "       (name it exactly: $repo  — do NOT add a README/.gitignore)"
    echo "    2) Then run, from inside $dir:"
    echo "         git remote add origin https://github.com/$ORG/$repo.git"
    echo "         git push -u origin main"
  fi
done

echo ""
echo "All done. Tell SodClaw \"refresh git state\" afterward so the dashboard updates."
