# Pi Scripts
This directory contains all the scripts needed to initialise and re-initialise a raspberry Pi image from scratch, or when something goes wrong.

## Brand new Raspbian image
At the beginning, you will likely have a Raspbian image that only has an internet connection.
We need to install the necessary packages and configurations, and we can do that with the scripts in this directory:

1. Pull the repository and enter into the installation directory
   ```bash
   cd ~/Downloads
   git clone https://github.com/mrontio/ic-rpi.git
   cd ic-rpi/pi-init
   ```

2. Run the initialisation script
   ```bash
   ./initialise.sh
   ```
   The script will:
   - Create the necessary changes in raspi-config [pi-conig.sh](./pi-config.sh)
   - Update & install necessary packages [apt.sh](./apt.sh)
   - Create a virtual environment [venv.sh](./venv.sh)
   - Install the packages in that virtual environment [pip.sh](./pip.sh)
   - Add the virtual environment to your environment file (.bashrc) [bashrc.sh](./bashrc.sh)

3. And Voilà, you have a system ready to hack on.

## Re-creating the virtual environment
Broke your pip installation? Don't worry, you can get back to a prepared virtual environment by running the following:

TODO!
