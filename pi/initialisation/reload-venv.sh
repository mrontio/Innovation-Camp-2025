#!/bin/bash

VENV_PATH="$HOME/hackathon-venv"

scripts/venv.sh $VENV_PATH
scripts/pip.sh $VENV_PATH

printf "\n\nvenv reloaded. Either log in or log back our, or run\nsource $VENV_PATH/bin/activate\nto activate the new environment.\n"
