sh
if [ -z "$1" ]; then
  echo "Error: VENV_PATH argument not provided."
  exit 1
fi

VENV_PATH="$1"

if [ ! -d "$VENV_PATH" ] || [ ! -x "$VENV_PATH/bin/python" ]; then
  echo "Error: $VENV_PATH is not a valid virtual environment."
  exit 1
fi

if [ ! -f "config/requirements.txt" ]; then
  echo "Error: config/requirements.txt not found."
  exit 1
fi

"$VENV_PATH/bin/pip" install -r config/requirements.txt
exit 0
