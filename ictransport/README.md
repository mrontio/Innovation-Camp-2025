# ictransport -- A communication layer between the Pi and Iridis
<p align="center"><img src="./img/diagram.png" alt="ictransport diagram" title="diagram" width="400" height="400"></p>

To simplify the hackathon for you, we decided to create a semi-transparent layer to communicate numpy objects from Pi to HPC and back with the help of your laptop.

## Startup Procedure (**important**)
As this was written in about 24 hours of work, there is a huge dependency on the order of starting each process. From now on, make sure to start them as pictured:

<p align="center"><img src="./img/startup.png" alt="startup diagram" title="startup" width="400" height="400"></p>

1. The laptop is the central puzzle piece to this, make sure to start it first.
2. The HPC is typically the listener. Start in second.
3. The Pi requests from Iridis. Start it last, or whenever you need something processed.

## Installation
You need to install ictransport on your *HPC instance* and *your laptop* to enable this communication layer (the Pi already has it installed).
1. On your laptop
   1. (Windows) Create a WSL to run Linux commands on (sorry windows users).
   2. Connect to [GlobalProtect](https://sotonproduction.service-now.com/serviceportal?id=kb_article_view&sys_kb_id=f04106b747e4d5583035862c736d43a2).
   3. Clone this repository
      ```
      cd Downloads
      git clone https://github.com/mrontio/Innovation-Camp-2025.git
      cd Innovation-Camp-2025
      ```
   4. Create a virtial environment just for this.
      ```
      python -m venv ~/Downloads/ictransport-venv
      source ~/Downloads/ictransport-venv/bin/activate
      ```
   5. Install ictransport to the venv
      ```
      pip install -e .
      ```
   6. Edit [examples/laptop_template.py](./examples/laptop_template.py) with your credentials
      ```
      pi_username = ""
      pi_address = ""
      pi_share_path = "" # Please use an absolute path

      hpc_username = ""
      hpc_address = ""
      hpc_share_path = "" # Please use an absolute path
      ```
   7. Run [examples/laptop_template.py](./examples/laptop_template.py) & edit as needed for your demonstrator.
      ```
      cd examples
      python laptop_template.py
      >>> Initialising Laptop!
      >>> Laptop: A single file transport has been completed!
      ```

2. On Iridis
   1. Login
      ```
      ssh <user>@<address> # This is a TODO
      ```
   2. Git clone this repository
      ```
      cd Downloads
      git clone https://github.com/mrontio/Innovation-Camp-2025.git
      cd Innovation-Camp-2025
      ```
   3. Create a new virtual environment, or re-use the one you have created
      ```
      module load python
      python -m venv ~/hackathon-venv
      source ~/hackathon-venv/bin/activate
      ```
   4. Install this package into the venv
      ```
      pip install -e ./
      ```
   5. Transfer files from your code with these functions, as can be seen in [examples/hpc_template.py](./examples/hpc_template.py).
      ```
      # Create a NodeTransport object
      hpc = NodeTransport(pi=False, share_path=hpc_share_path)
      # Await for an input
      received_input = hpc.listen()
      # Do some calculations
      processed_output = received_input * 2
      # Send it back to the Pi
      hpc.send(processed_output)
      ```

3. On the Pi
   1. The `hackathon-venv` that you [initialised after signing off](../pi/initialisation) already contains ictransport.
   2. Use it within your code, such as in [examples/pi_template.py](./example/pi_template.py).
