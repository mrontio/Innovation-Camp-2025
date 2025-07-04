#/bin/bash
if [ -z "$1" ]; then
  echo "Usage: $0 <VENV_PATH>"
  exit 1
fi

VENV_PATH="$1"
STRING="source \"$VENV_PATH/bin/activate\"  # Added by venv activation script"

if grep -Fxq "$STRING" ~/.bashrc; then
  echo "Venv path already added to .bashrc"
  exit 1
fi

echo "$STRING" >> ~/.bashrc
exit 0
