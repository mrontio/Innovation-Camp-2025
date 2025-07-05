import paramiko
from abc import ABC, abstractmethod
import errno
import numpy as np
import io
import re
import time
import os
from pathlib import Path

# TODO: Better way to identifying the destination sending to automatically

class ICTransport(ABC):

    def __init__(self,
                 timeout_s: float = 60,
                 sleep_time: float = 10):

        self.timeout_s = timeout_s
        self.sleep_time = sleep_time
    
    def not_timeout(self, start_time, timeout_s):
        if timeout_s:
            return (time.time() - start_time < timeout_s)
        else:
            return True
    
    @abstractmethod    
    def append_file(self, sftp, sync_file, string) -> None:
        pass
    
    @abstractmethod
    def read_last(self, sftp, sync_file) -> str:
        pass

    @abstractmethod
    def clear_sync(self, sftp, sync_file) -> None:
        pass

    @abstractmethod
    def send(self, n, pi) -> bool:
        pass

    @abstractmethod
    def listen(self, pi, timeout_s=None) -> np.array:
        pass

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

        super().__init__(timeout_s, sleep_time)


        self.pi_username = pi_username
        self.hpc_username = hpc_username
        self.pi_address = pi_address
        self.hpc_address = hpc_address

        self.pi_share_path = pi_share_path.rstrip("/")
        self.hpc_share_path = hpc_share_path.rstrip("/")

        self.pi_sync = f"{pi_share_path}/pi_sync.log"
        self.hpc_sync = f"{hpc_share_path}/hpc_sync.log"

        self.retries_max = 5

        print(f"Pi connection: attempt {pi_username}@{pi_address}.")
        # Setup Pi connection and sync file
        self.pi_client, self.pi_sftp = self.__connectSFTP(pi_username, pi_address, verbose=False) # Defines: [self.client, self.sftp]
        if not self.rexists(self.pi_sftp, self.pi_share_path):
            self.pi_sftp.mkdir(self.pi_share_path)
        if not self.rexists(self.pi_sftp, self.pi_sync):
            with self.pi_sftp.open(self.pi_sync, "w") as file:
                pass
        print(f"Pi connection: success.")


        # Setup HPC connection and sync file
        print(f"HPC connection: attempt {hpc_username}@{hpc_address}.")
        self.hpc_client, self.hpc_sftp = self.__connectSFTP(hpc_username, hpc_address, verbose=False) # Defines: [self.client, self.sftp]

        if not self.rexists(self.hpc_sftp, self.hpc_share_path):
            self.hpc_sftp.mkdir(self.hpc_share_path)
        if not self.rexists(self.hpc_sftp, self.hpc_sync):
            with self.hpc_sftp.open(self.hpc_sync, "w") as file:
                pass
        print(f"HPC connection: success.")


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
                    print(f"Connection: {username}@{address}.")
                client = paramiko.SSHClient()
                client.load_system_host_keys()
                client.connect(address, username=username, timeout=self.timeout_s, channel_timeout=self.timeout_s)
                if verbose:
                    print(f"Connection: success.")

                # Establish SFTP channel
                if verbose:
                    print(f"SFTP: {username}@{address}.")
                sftp = client.open_sftp()
                if verbose:
                    print("SFTP: success.")

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
    
    def __reconnectSFTP(self, pi):
        print("error: SSH connection lost, trying to re-establish...")
        if pi:
            self.pi_sftp.close()
            self.pi_client.close()
            self.pi_client, self.pi_sftp = self.__connectSFTP(self.pi_username, self.pi_address, verbose=True)
        else:
            self.hpc_sftp.close()
            self.hpc_client.close()
            self.hpc_client, self.hpc_sftp = self.__connectSFTP(self.hpc_username, self.hpc_address, verbose=True)
      
    def append_file(self, sftp, sync_file, string):
        file = sftp.file(sync_file, "a", -1)
        file.write(f"\nLaptop: {string}")
        file.flush()
        file.close()
    
    def read_last(self, sftp, sync_file):
        file = sftp.file(sync_file, "r")
        lines = file.readlines()
        if len(lines) > 1:
            out = lines[-1].strip()
        else: # File is empty
            out = ""
        file.close()
        return out

    def clear_sync(self, sftp, sync_file):
        try:
            with sftp.open(sync_file, "w") as file:
                pass
            print(f"Sync file {sync_file} has been successfully cleared")
        except Exception as e:
            print(f"Could not clear file {sync_file} due: {e}")

    def __uniqueFileName(self, sftp, share_path) -> str:
        paths = sftp.listdir(share_path)
        pattern = re.compile(r"^([0-9]+)\.npy$")
        filtered = [p for p in paths if pattern.match(p)]
        if filtered:
            filtered.sort(key=lambda x: int(pattern.match(x).group(1)), reverse=True)
            m = pattern.match(filtered[0])
            num = int(m.group(1)) + 1
        else:
            num = 1
        return f"{num}.npy"

    def send(self, n, pi) -> bool:
        # Initialiase the buffer
        # - Acts as a file for np to write to
        if pi:
            sftp = self.pi_sftp
            sync_file = self.pi_sync
            share_path = self.pi_share_path
        else:
            sftp = self.hpc_sftp
            sync_file = self.hpc_sync
            share_path =  self.hpc_share_path
        
        buf = io.BytesIO()
        np.save(buf, n)
        buf.seek(0)

        # Retry loop
        done = False
        # Put buffer onto new file path with unique file name.
        new_file_name = self.__uniqueFileName(sftp, pi)
        new_file_path = share_path + "/" + new_file_name
        while not done:
            try:
                sftp.putfo(buf, new_file_path)
                done = True
            except (paramiko.SSHException, TimeoutError) as e:
                self.__reconnectSFTP(pi)

        return done
    
    def listen(self, pi, timeout_s=None) -> np.array:
        if pi:
            sftp = self.pi_sftp
            sync_file = self.pi_sync
            share_path = self.pi_share_path
        else:
            sftp = self.hpc_sftp
            sync_file = self.hpc_sync
            share_path =  self.hpc_share_path
            
        # Take start time of listen() call
        start_time = time.time()

        # Create buffer for np to write into
        buf = io.BytesIO()
        while self.not_timeout(start_time, timeout_s):
            try:
                # List the paths and sort them based on modification time (f.st_mtime)
                paths = sftp.listdir_attr(share_path)
                new_files = [f.filename for f in paths if f.st_mtime > start_time]
                if len(new_files) > 0:
                    # If we found files modified later than our start time:
                    # take the first one and return it.
                    new_file = new_files[0]
                    new_file_path = share_path + "/" + new_file
                    sftp.getfo(new_file_path, buf)
                    buf.seek(0)
                    array = np.load(buf)
                    return array
            except (paramiko.SSHException, TimeoutError) as e:
                self.__reconnectSFTP(pi)
            print("Timeout! No file was received back")
            return None

class NodeTransport(ICTransport):
    def __init__(self,
                 pi: bool,
                 share_path: str = "~/ic-transport", # Please always provide absolute full path
                 timeout_s: float = 60,
                 sleep_time: float = 10):

        super().__init__(timeout_s, sleep_time)
        self.share_path = share_path.rstrip("/")
        self.sync_file = f"{share_path}/hpc_sync.log"

        if not os.path.exists(self.share_path):
            os.makedirs(self.share_path)

        if not os.path.exists(self.sync_file):
            Path(self.sync_file).touch()

    def __uniqueFileName(self) -> str:
        paths = os.listdir(self.share_path)
        pattern = re.compile(r"^([0-9]+)\.npy$")
        filtered = [p for p in paths if pattern.match(p)]
        if filtered:
            filtered.sort(key=lambda x: int(pattern.match(x).group(1)), reverse=True)
            m = pattern.match(filtered[0])
            num = int(m.group(1)) + 1
        else:
            num = 1
        return f"{num}.npy"

    def send(self, n, pi=None) -> bool:
        new_file_name = self.__uniqueFileName()
        path = self.share_path + "/" + new_file_name
        np.save(path, n)
        
        return True
    
    def listen(self, pi=None, timeout_s=None) -> np.array:
        start_time = time.time()

        while self.not_timeout(start_time, timeout_s):
            paths = Path(self.share_path).iterdir()
            new_files = [f.name for f in paths if f.stat().st_mtime > start_time]
            if len(new_files) > 0:
                new_file = new_files[0]
                array = np.load(self.share_path + "/" + new_file)

                return array
            
            time.sleep(self.sleep_time)