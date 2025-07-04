#!/bin/sh

VENV_PATH="$HOME/hackathon-venv"

descriptions=(
    "Configure Raspberry Pi"
    "Install required APT packages"
    "Set up Python virtual environment"
    "Install pip requirements"
    "Configure .bashrc"
)

scripts="pi-config.sh apt.sh venv.sh pip.sh bashrc.sh"

i=0
for script in $scripts; do
    desc="${descriptions[$i]}"
    echo "\n=============================================="
    echo "Running $script: $desc"
    echo "==============================================\n"

    if ! ./"$script" "$VENV_PATH"; then
        echo "Error: $script failed. Figure it out by looking into $script or asking Michail."
        exit 1
    fi
    i=$((i + 1))
done

echo "Initialisation completed sucessfully. Enjoy the hackathon."
