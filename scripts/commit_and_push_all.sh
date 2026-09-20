#!/usr/bin/env bash
#
# SodClaw — commit + push all repos with uncommitted work, and scrub the
# token-embedded Gazette remote. Generated 2026-06-13.
#
# Run from anywhere:  bash ~/Meatbag_Labs/SodClaw/scripts/commit_and_push_all.sh
# It will SHOW you each diff/status and PAUSE for a yes before committing.
# Nothing is force-anything. Review as you go.
#
set -uo pipefail

ML="$HOME/Meatbag_Labs"

# repo dir | clean remote url | commit message
REPOS=(
  "$ML/SodClaw|https://github.com/kevin-sotka/SodClaw.git|chore: sweep updates — novel progress, Foundry tracked, Wall shelved, dashboard rebuild"
  "$ML/thegridirongazette|https://github.com/kevin-sotka/thegridirongazette.git|chore: commit pending Gazette changes"
  "$ML/RT1|https://github.com/kevin-sotka/Riventide.git|chore: commit pending Riventide changes (171-file backlog)"
  "$ML/AI-company-trail|https://github.com/kevin-sotka/AI-company-trail.git|chore: commit pending AI Company Trail changes"
)

confirm() { read -r -p "$1 [y/N] " a; [[ "$a" == "y" || "$a" == "Y" ]]; }

for entry in "${REPOS[@]}"; do
  IFS='|' read -r DIR CLEAN_REMOTE MSG <<< "$entry"
  echo
  echo "=================================================================="
  echo "REPO: $DIR"
  echo "=================================================================="
  if [[ ! -d "$DIR/.git" ]]; then
    echo "  ⚠ no .git here — skipping"; continue
  fi
  cd "$DIR" || { echo "  ⚠ can't cd — skipping"; continue; }

  # --- scrub token from remote if present ---
  CUR="$(git remote get-url origin 2>/dev/null || echo '')"
  if [[ "$CUR" == *"@github.com"* ]]; then
    echo "  🔒 origin has credentials embedded in the URL. Replacing with clean URL:"
    echo "       $CLEAN_REMOTE"
    git remote set-url origin "$CLEAN_REMOTE"
    echo "  ✓ remote cleaned. (Rotate that token on GitHub — see note at end.)"
  fi

  # --- show what's pending ---
  if [[ -z "$(git status --porcelain)" ]]; then
    echo "  ✓ working tree clean — nothing to commit."
  else
    git status --short
    echo
    if confirm "  Stage ALL and commit the above in $(basename "$DIR")?"; then
      git add -A
      git commit -m "$MSG"
      echo "  ✓ committed."
    else
      echo "  ↷ skipped commit."
    fi
  fi

  # --- push ---
  if confirm "  Push $(basename "$DIR") to origin/$(git rev-parse --abbrev-ref HEAD 2>/dev/null)?"; then
    git push origin HEAD && echo "  ✓ pushed." || echo "  ⚠ push failed — check auth (use a credential helper, not a URL token)."
  else
    echo "  ↷ skipped push."
  fi
done

echo
echo "=================================================================="
echo "DONE. Security follow-ups:"
echo "  1. The Gazette token is no longer in any remote URL, but it still"
echo "     EXISTS on GitHub. Rotate it: GitHub → Settings → Developer"
echo "     settings → Personal access tokens → revoke the old one,"
echo "     generate a fresh one if needed."
echo "  2. Store creds via a helper instead of the URL:"
echo "       git config --global credential.helper osxkeychain"
echo "=================================================================="
