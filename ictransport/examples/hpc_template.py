from ictransport import NodeTransport

# Ensure to use the same file used when initialising Laptop
hpc_share_path = "" # Please use an absolute path

print("Initialising HPC!")
hpc = NodeTransport(pi=False, share_path=hpc_share_path) # You can also adjust the timeout and sleep time using timeout_s= and sleep_time=, respectively.

# Receive data observed by pi from laptop
received_input = hpc.listen()

# Your code that needs hpc should replace the line below
processed_output = received_input * 2

# Send processed data to pi through the laptop
hpc.send(processed_output)

print("HPC: A file has been receved, process and sent back!")