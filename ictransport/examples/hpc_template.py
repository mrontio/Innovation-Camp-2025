from ictransport import NodeTransport
import numpy as np

hpc_share_path = ""

# Create the communication object
hpct = NodeTransport(pi=False, share_path=hpc_share_path)

# Service loop
while True:
    # Wait for the Pi to give you something to do
    pi_input = hpct.listen()

    print(f"Received {pi_input.shape}. Processing")

    # Do some big calculation with your big HPC capabilities
    processed_output = pi_input * 2

    print(f"Processing complete. Returning to sender.")

    # Send it over
    hpct.send(processed_output)
