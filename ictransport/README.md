## How are we synchronising?
### Phase Zero: Initialise Connections
   1. [x] Laptop.init():
      - [t] Pi SFTP Connection
      - [t] HPC SFTP Connection

#### Observe a state using Pi

### Phase One: Read from Pi
   1. [x] Laptop.listen(pi):
      - Await 'Pi: 0001-sent'
      - Receive '0001.npy'
      - Write(pi_sync) 'Laptop: 0001-received'
   2. [x] Pi.send()
      - Write '0001.npy'
      - Write(pi_sync) 'Pi: 0001-sent'
      - [t] Awaiting 'Laptop: 0001-received'
      - Return success

### Phase Two: Send to HPC
   1. [x] Laptop.send(hpc):
      - Write '0001.npy'
      - Write(hpc_sync) 'Laptop: 0001-sent'
      - [t] Awaiting 'HPC: 0001-received'
      - Return success
   2. [x] HPC.listen()
      - Await 'Laptop: 0001-sent'
      - Receive '0001.npy'
      - Write(hpc_sync) 'HPC: 0001-received'
      - Return as np array

#### Process '0001.npy' in HPC

### Phase Three: Read from HPC
   1. [x] Laptop.listen(hpc):
      - Await 'HPC: 0001-out-sent'
      - Receive '0001-out.npy'
      - Return as np array.
   2. [x] HPC.send()
      - Write '0001-out.npy'
      - Write(hpc_sync) 'HPC: 0001-out-sent'
      - [t] Awaiting 'Laptop: 0001-out-received'
      - Return success

### Phase Four: Send to Pi
   1. [x] Laptop.send(pi):
      - Write '0001-out.npy'
      - Write(pi_sync) 'Laptop: 0001-out-sent'
      - [t] Awaiting 'Pi: 0001-out-received'
      - Return success
   2. [x] Pi.listen()
      - Await 'Laptop: 0001-out-sent'
      - Receive '0001-out.npy'
      - Write(pi_sync) 'Pi: 0001-out-received'
      - Return as np array

#### Print the returned np array from HPC or further process it

#### Laptop.close_connection() for Pi and HPC SFTP Connections when done

## Failure Modes
   - [t] = needs some sort of timeout for retry