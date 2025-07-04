sh
#!/bin/sh

if [ -z "$1" ]; then
  echo "venv.sh: error: VENV_PATH argument is required"
  exit 1
fi

VENV_PATH="$1"

if [ -d "$VENV_PATH" ]; then
  if [ -x "$VENV_PATH/bin/python" ]; then
    OLD_PACKAGES="$("$VENV_PATH/bin/pip" freeze)"
  fi
  rm -rf -- "$VENV_PATH"
fi

python -m venv --system-site-packages "$VENV_PATH"
exit 0
