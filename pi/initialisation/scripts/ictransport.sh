#!/bin/sh

if [ -z "$1" ]; then
  echo "Usage: $0 VENV_PATH"
  exit 1
fi

VENV_PATH="$1"
SOURCE="https://github.com/mrontio/Innovation-Camp-2025.git"  # replace with your actual source repo
DOWNLOADS="$HOME/Downloads"
REPO_NAME=$(basename "$SOURCE" .git)

if [ ! -d "$DOWNLOADS/$REPO_NAME/.git" ]; then
  git clone "$SOURCE" "$DOWNLOADS/$REPO_NAME"
fi

"$VENV_PATH/bin/pip" install -e "$DOWNLOADS/$REPO_NAME"
exit 0
