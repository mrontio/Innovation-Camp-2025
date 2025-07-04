from ictransport import LaptopTransport
import numpy as np

pi_username = ""
pi_address = ""

hpc_username = ""
hpc_address = ""

print("Initialising Both!")
pit = LaptopTransport(pi_username, hpc_username, pi_address, hpc_address, "./pi-ic-transport", "./hpc-ic-transport")

print("Done")