#!/bin/sh

VENV_PATH="$HOME/hackathon-venv"

scripts="scripts/pi-config.sh scripts/apt.sh scripts/venv.sh scripts/pip.sh scripts/ictransport.sh scripts/bashrc.sh"

for script in $scripts;
do

    if [ -z "$script" ]; then
        echo "\n\nError: script $script is missing, please clone the repository again."
        exit 1
    fi

    echo
    echo "=============================================="
    echo "Running $script"
    echo "=============================================="
    echo

    if ! ./"$script" "$VENV_PATH"; then
        echo "\n\nError: $script failed. Figure it out by looking into $script or asking Michail."
        exit 1
    fi
done


echo "\n\nInitialisation completed sucessfully. I will now have to reboot, and you will be ready to go.\nHave fun with the hackathon."


for i in $(seq 10 -1 1); do
    bars=$((20 - (2 * (10 - i))))
    no_bars=$((20 - bars))
    # Clear the line
    printf '\r'
    printf ' %.0s' {1..100}
    printf '\r'
    # Print the bar
    printf 'REBOOTING IN %d SECONDS: [  ' $i
    eval printf '=%.0s' {1..$bars}
    eval printf '\ %.0s' {1..$no_bars}
    printf ']'
    sleep 1
done

sudo reboot
