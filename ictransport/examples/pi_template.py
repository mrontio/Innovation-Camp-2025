from ictransport import NodeTransport
import numpy as np
import getpass

# Ensure to use the same file used when initialising Laptop
username = getpass.getuser()
pi_share_path = f"/home/{username}/ictransport" # Please use an absolute path

print("Initialising Pi!")
pi = NodeTransport(pi=True, share_path=pi_share_path)

# Imaginary sensor data after observing some data.
# Your code that uses the pi and its sensors should replace the line below
camera_output = np.ones((128, 128))

# Send observed data to laptop to be sent to hpc
pi.send(camera_output)

# Receive processed data by the hpc through the laptop
received_output = pi.listen()

print("Pi: A state has been observed and processed file!")

# Verify it's correct
# The function on hpc template is simply X * 2
print(f"Output coincides? {camera_output}\n\n{received_output}")
