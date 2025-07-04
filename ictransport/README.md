## How are we synchronising?
- send(path: str, n: np.array): Bool
- listen(path: str, timeout=None: int): (np.array, Bool)
- Ideal flow:
Phase one: Read from Pi
   1. [ ] Laptop.listen(pi):
      - [t] Pi SFTP Connection
      - Await '0001-sent'
      - File '0001.npy' received
      - Write(pi_sync) '0001-received'
   2. [ ] Pi.send()
      - File '0001.npy' written'
      - Write(pi_sync) '0001-sent'
      - [t] Awaiting '0001-received'
      - File '0001-recevied' exists
      - Return success

Phase two: Send to HPC
   1. [ ] Laptop.send(hpc):
      - [t] HPC SFTP Connection
      - File '0001.npy' written'
      - Write(hpc_sync) '0001-sent'
      - [t] Awaiting '0001-received'
      - File '0001-recevied' exists
      - Return success
   2. [ ] HPC.listen()
      - Await '0001-sent'
      - File '0001.npy' received
      - Write '0001-received'

Process '0001.npy'

Phase three: Read from HPC
   1. [ ] HPC.send()
      - Write (fully) '0001-out.npy'
      - Write(hpc_sync) '0001-out-sent'
   2. [ ] Laptop.listen(hpc):
      - Await '0001-out-sent'
      - Receive '0001-out.npy'
      - Return as np array.

Phase four: Send to Pi
   1. [ ] Laptop.send(pi):
      - File '0001-out.npy' written'
      - Write(pi_sync) '0001-out-sent'
      - [t] Awaiting '0001-received'
      - File '0001-out-recevied' exists
      - Return success
   2. [ ] Pi.listen()
      - Await '0001-out-sent'
      - Receive '0001-out.npy'
      - Return as np array.

Failure modes
   - [t] = needs some sort of timeout for retry