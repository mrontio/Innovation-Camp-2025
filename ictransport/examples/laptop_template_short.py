from ictransport import LaptopTransport
import numpy as np

pi_username = ""
pi_address = ""
pi_share_path = "" # Please use an absolute path

hpc_username = ""
hpc_address = ""
hpc_share_path = "" # Please use an absolute path

print("Initialising Laptop!")
laptop = LaptopTransport(pi_username, hpc_username, pi_address, hpc_address, pi_share_path, hpc_share_path)

# Ensure that all sync files all empty
laptop.clear_sync(pi=True)
laptop.clear_sync(pi=False)

hpc_output = np.ones((128,128))
# Send received data to pi
laptop.send(hpc_output, pi=True)

print("Laptop: A single file transport has been completed!")
