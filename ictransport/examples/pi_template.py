from ictransport import NodeTransport
import numpy as np

pi_share_path = ""

# Create the communication object
pi = NodeTransport(pi=True, share_path=pi_share_path)

print("Creating camera outputs")

# Imaginary sensor data
camera_output = np.ones((128, 128))

print("Sending...")
# Send it over
pi.send(camera_output)

print("Listening...")

# Wait for the server to process it
hpc_output = pi.listen()

print("Done")

# Verify it's correct
# The function on HPC is simply X * 2
print(f"Output coincides? {camera_output}\n{hpc_output}")
