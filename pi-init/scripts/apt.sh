#!/bin/bash

# This script updates the system and installs the necessary packages for the hackathon.

sudo apt update
sudo apt upgrade -y

# Install required packages
sudo apt install -y libcap-dev
