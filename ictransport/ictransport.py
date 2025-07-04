import paramiko
from abc import ABC, abstractmethod
import errno

class ICTransport(ABC):

    def __init__(self,
                 share_path: str = "~/ic-transport", # Please always provide absolute full path
                 timeout_s: float = 60,
                 sleep_time: float = 10):
        
        self.share_path = share_path
        self.timeout_s = timeout_s
        self.sleep_time = sleep_time

class LaptopTransport(ICTransport):
    def __init__(self,
                 pi_username: str,
                 hpc_username: str,
                 pi_address: str,
                 hpc_address: str,
                 pi_share_path: str = "~/ic-transport", # Please always provide absolute full path
                 hpc_share_path: str = "~/ic-transport", # Please always provide absolute full path
                 timeout_s: float = 60,
                 sleep_time: float = 10):
        
        super().__init__("", timeout_s, sleep_time)


        self.pi_username = pi_username
        self.hpc_username = hpc_username
        self.pi_address = pi_address
        self.hpc_address = hpc_address

        self.pi_share_path = pi_share_path.rstrip("/")
        self.hpc_share_path = hpc_share_path.rstrip("/")

        self.pi_sync = f"{pi_share_path}/pi_sync.log"
        self.hpc_sync = f"{hpc_share_path}/hpc_sync.log"

        self.retries_max = 5

        # Setup Pi connection and sync file
        self.pi_client, self.pi_sftp = self.__connectSFTP(pi_username, pi_address) # Defines: [self.client, self.sftp]
        if not self.rexists(self.pi_sftp, self.pi_share_path):
            self.pi_sftp.mkdir(self.pi_share_path)
        if not self.rexists(self.pi_sftp, self.pi_sync):
            with self.pi_sftp.open(self.pi_sync, "w") as file:
                pass

        # Setup Pi connection and sync file
        self.hpc_client, self.hpc_sftp = self.__connectSFTP(hpc_username, hpc_address) # Defines: [self.client, self.sftp]
        if not self.rexists(self.hpc_sftp, self.hpc_share_path):
            self.hpc_sftp.mkdir(self.hpc_share_path)
        if not self.rexists(self.hpc_sftp, self.hpc_sync):
            with self.hpc_sftp.open(self.hpc_sync, "w") as file:
                pass
        
    def __connectSFTP(self, username, address, verbose=True):
        done = False
        retries = 0
        client = None
        sftp = None
        while not done:
            try:
                # Retry condition
                if retries > self.retries_max:
                    print(f"error: ictransport could not establish a connection within {self.retries_max} retries. Quitting program.")
                    exit(1)

                # Establish SSH Connection
                if verbose:
                    print("Trying SSH...")
                client = paramiko.SSHClient()
                client.load_system_host_keys()
                client.connect(address, username=username, timeout=self.timeout_s, channel_timeout=self.timeout_s)
                if verbose:
                    print("SSH Connected.")

                # Establish SFTP channel
                if verbose:
                    print("Trying SFTP...")
                sftp = client.open_sftp()
                if verbose:
                    print("SFTP Connected.")

                channel = sftp.get_channel()
                channel.settimeout(self.timeout_s)

                done = True
            except paramiko.AuthenticationException as e:
                print(f"Authentication failed: {e}")
            except paramiko.SSHException as e:
                print(f"SSH error: {e}")
            except (IOError, OSError) as e:
                print(f"File I/O error: {e}")
            except Exception as e:
                print(f"Could not connect: {e}")
        
        return client, sftp
    
    # https://stackoverflow.com/questions/850749/check-whether-a-path-exists-on-a-remote-host-using-paramiko
    def rexists(self, sftp, path):
        """os.path.exists for paramiko's SCP object"""
        try:
            sftp.stat(path)
        except IOError as e:
            if e.errno == errno.ENOENT:
                return False
            raise
        else:
            return True