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
# TODO: Specify locations of log files when application starts
# TODO: Ensure default of all timeouts is not None
# TODO: Add timeout_s and sleep_time setters and getters?
# TODO: Add better timeout to listening and before listening so both don't share and send
# TODO: Add sleep throughout

class ICTransport(ABC):

    def __init__(self,
                 timeout_s: float,
                 sleep_time: float):

        self.timeout_s = timeout_s
        self.sleep_time = sleep_time

    def not_timeout(self, start_time):
        if self.timeout_s:
            return (time.time() - start_time < self.timeout_s)
        else:
            return True

    @abstractmethod
    def append_file(self, string, pi) -> None:
        pass

    @abstractmethod
    def read_last(self, pi) -> str:
        pass

    @abstractmethod
    def read_sync_file(self, pi) -> str:
        pass

    @abstractmethod
    def clear_sync(self, pi) -> None:
        pass

    @abstractmethod
    def awaiting_after_send(self, expected_last_line, start_time, pi) -> bool:
        pass

    @abstractmethod
    def send(self, n, pi) -> bool:
        pass

    @abstractmethod
    def awaiting_before_listen(self, start_time, pi) -> str:
        pass

    @abstractmethod
    def listen(self, pi) -> np.array:
        pass


class LaptopTransport(ICTransport):
    def __init__(self,
                 pi_username: str,
                 hpc_username: str,
                 pi_address: str,
                 hpc_address: str,
                 pi_share_path: str = "~/ic-transport", # Please always provide absolute full path
                 hpc_share_path: str = "~/ic-transport", # Please always provide absolute full path
                 timeout_s: float = None,
                 sleep_time: float = 1):

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

    def close_connection(self, pi) -> None:
        if pi:
            self.pi_sftp.close()
            self.pi_client.close()
        else:
            self.hpc_sftp.close()
            self.hpc_client.close()

    def get_node_info(self, pi):
        if pi:
            node_type = "Pi"
            sftp = self.pi_sftp
            sync_file = self.pi_sync
            share_path = self.pi_share_path
        else:
            node_type = "HPC"
            sftp = self.hpc_sftp
            sync_file = self.hpc_sync
            share_path = self.hpc_share_path

        return node_type, sftp, sync_file, share_path

    def __reconnectSFTP(self, pi):
        print("error: SSH connection lost, trying to re-establish...")
        self.close_connection(pi)
        if pi:
            self.pi_client, self.pi_sftp = self.__connectSFTP(self.pi_username, self.pi_address, verbose=True)
        else:
            self.hpc_client, self.hpc_sftp = self.__connectSFTP(self.hpc_username, self.hpc_address, verbose=True)

    def append_file(self, string, pi):
        node_type, sftp, sync_file, share_path = self.get_node_info(pi)
        file = sftp.file(sync_file, "a", -1)
        file.write(f"\nLaptop: {string}")
        file.flush()
        file.close()

    def read_sync_file(self, pi=None) -> str:
        node_type, sftp, sync_file, share_path = self.get_node_info(pi)
        file = sftp.file(sync_file, "r")
        lines = file.read().decode().strip().split("\n")
        file.close()
        return lines

    def read_last(self, pi):
        node_type, sftp, sync_file, share_path = self.get_node_info(pi)
        file = sftp.file(sync_file, "r")
        lines = file.read().decode().strip().split("\n")
        if len(lines) > 0:
            out = lines[-1].strip()
        else: # File is empty
            out = ""
        file.close()
        return out

    def clear_sync(self, pi):
        node_type, sftp, sync_file, share_path = self.get_node_info(pi)
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

    def awaiting_after_send(self, expected_last_line, start_time, pi):
        """Ensure that a file is received successfully
        Uses the same global timeout"""

        while self.not_timeout(start_time):
            last_lines = self.read_sync_file(pi)
            print(last_lines)
            print(expected_last_line)
            if expected_last_line in last_lines:
                return True
            time.sleep(self.sleep_time)

        return False

    def send(self, n, pi) -> bool:
        # Initialiase the buffer
        # - Acts as a file for np to write to
        node_type, sftp, sync_file, share_path = self.get_node_info(pi)

        start_time = time.time()

        buf = io.BytesIO()
        np.save(buf, n)
        buf.seek(0)
        print("Laptop: Sending...")

        # Put buffer onto new file path with unique file name.
        file_name = self.__uniqueFileName(sftp, share_path)
        file_path = share_path + "/" + file_name
        while self.not_timeout(start_time):
            try:
                sftp.putfo(buf, file_path)

                # Write acknowledgement
                self.append_file(f"{share_path}/{file_name.replace('.npy', '')}-sent", pi)

                print(f"Laptop: Waiting for confirmation from {node_type}")
                if self.awaiting_after_send(f"{node_type}: {share_path}/{file_name.replace('.npy', '')}-received", start_time, pi):
                    print(f"Laptop: File was sent sucessfully to {node_type}")
                    return True
            except (paramiko.SSHException, TimeoutError) as e:
                self.__reconnectSFTP(pi)

        print(f"Laptop: Timeout! It seems that the file was not sent successfully")
        return False

    def awaiting_before_listen(self, start_time, pi):
        """Ensure that a file is sent before listening
        Uses the same global timeout"""
        if pi:
            node_type = "Pi"
            share_path = self.pi_share_path
        else:
            node_type = "HPC"
            share_path = self.hpc_share_path

        while self.not_timeout(start_time):
            last_line = self.read_last(pi)
            if last_line.startswith(f"{node_type}: ") and last_line.endswith("-sent"):
                return last_line.replace(f"{node_type}: ", "").replace("-sent", "").replace(f"{share_path}/", "").strip() + ".npy"

            time.sleep(self.sleep_time)

        return ""

    def listen(self, pi) -> np.array:
        node_type, sftp, sync_file, share_path = self.get_node_info(pi)

        # Take start time of listen() call
        start_time = time.time()

        print(f"Laptop: Waiting confirmation from {node_type} to start listening")
        file_to_listen = self.awaiting_before_listen(start_time, pi)
        if file_to_listen:
            print(f"Laptop: Confirmation received from {node_type}. Listening...")
            # Create buffer for np to write into
            buf = io.BytesIO()
            while self.not_timeout(start_time):
                try:
                    paths = sftp.listdir_attr(share_path)
                    files = [f.filename for f in paths if f.st_mtime > start_time]
                    if file_to_listen in files:
                        file_path = share_path + "/" + file_to_listen
                        sftp.getfo(file_path, buf)
                        buf.seek(0)
                        array = np.load(buf)

                        # Write acknowledgement
                        self.append_file(f"{share_path}/{file_to_listen.replace('.npy', '')}-received", pi)

                        return array
                except (paramiko.SSHException, TimeoutError) as e:
                    self.__reconnectSFTP(pi)

                time.sleep(self.sleep_time)
            print(f"Laptop: Timeout! No file was received back from {node_type}")
            return None
        else:
            print(f"Laptop: Timeout! No file was sent or at least communicated that it was sent from {node_type}")
            return None

class NodeTransport(ICTransport):
    def __init__(self,
                 pi: bool,
                 share_path: str = "~/ic-transport", # Please always provide absolute full path
                 timeout_s: float = None,
                 sleep_time: float = 1):

        super().__init__(timeout_s, sleep_time)
        self.share_path = share_path.rstrip("/")

        if pi:
            self.node_type = "Pi"
            self.sync_file = f"{share_path}/pi_sync.log"
        else:
            self.node_type = "HPC"
            self.sync_file = f"{share_path}/hpc_sync.log"

        print(f"Starting {self.node_type} Node")
        if not os.path.exists(self.share_path):
            os.makedirs(self.share_path)

        if not os.path.exists(self.sync_file):
            Path(self.sync_file).touch()
        print(f"{self.node_type} Node started.")

    def __uniqueFileName(self) -> str:
        paths = os.listdir(self.share_path)
        pattern = re.compile(r"^([0-9]+)\.npy$")
        filtered = [p for p in paths if pattern.match(p)]
        if filtered:
            filtered.sort(key=lambda x: int(pattern.match(x).group(1)), reverse=True)
            m = pattern.match(filtered[0])
            if self.node_type == "HPC":
                num = int(m.group(1))
            else:
                num = int(m.group(1)) + 1
        else:
            num = 1

        if self.node_type == "HPC":
            return f"{num}-out.npy"
        else:
            return f"{num}.npy"

    def append_file(self, string, pi=None) -> None:
        with open(self.sync_file, "a") as file:
            file.write(f"\n{self.node_type}: {string}")

    def read_last(self, pi=None) -> str:
        with open(self.sync_file, "r") as file:
            lines = file.read().strip().split("\n")
            if len(lines) > 0:
                out = lines[-1].strip()
            else:
                out = ""
        return out

    def read_sync_file(self, pi=None) -> str:
        with open(self.sync_file, "r") as file:
            lines = file.read().strip().split("\n")
        return lines

    def clear_sync(self, pi=None) -> None:
        try:
            with open(self.sync_file, "w") as file:
                pass
            print(f"{self.node_type} Node: Sync file {self.sync_file} has been successfully cleared")
        except Exception as e:
            print(f"{self.node_type} Node: Could not clear file {self.sync_file} due: {e}")

    def awaiting_after_send(self, expected_last_line, start_time, pi=None):
        """Ensure that a file is received successfully
        Uses the same global timeout"""

        while self.not_timeout(start_time):
            if expected_last_line in self.read_sync_file(pi):
                return True
            time.sleep(self.sleep_time)

        return False

    def send(self, n, pi=None):
        start_time = time.time()
        file_name = self.__uniqueFileName()
        path = self.share_path + "/" + file_name

        print(f"{self.node_type}: Sending...")
        while self.not_timeout(start_time):
            np.save(path, n)

            # Write acknowledgement
            self.append_file(f"{self.share_path}/{file_name.replace('.npy', '')}-sent", pi)

            print(f"{self.node_type}: Waiting for confirmation from Laptop")
            # Awaiting
            if self.awaiting_after_send(f"Laptop: {self.share_path}/{file_name.replace('.npy', '')}-received", start_time, pi):
                print(f"{self.node_type}: File was sent sucessfully to Laptop")
                return True

        print(f"{self.node_type}: Timeout! It seems that the file was not sent successfully")
        return False

    def awaiting_before_listen(self, start_time, pi=None):
        """Ensure that a file is sent before listening
        Uses the same global timeout"""
        while self.not_timeout(start_time):
            last_line = self.read_last(pi)
            if last_line.startswith("Laptop: ") and last_line.endswith("-sent"):
                return last_line.replace("Laptop: ", "").replace("-sent", "").replace(f"{self.share_path}/", "").strip() + ".npy"
            time.sleep(self.sleep_time)

        return ""

    def listen(self, pi=None) -> np.array:
        start_time = time.time()

        print(f"{self.node_type}: Waiting confirmation from Laptop to start listening")
        file_to_listen = self.awaiting_before_listen(start_time, pi)
        if file_to_listen:
            print(f"{self.node_type}: Confirmation received from Laptop. Listening...")
            while self.not_timeout(start_time):
                paths = Path(self.share_path).iterdir()
                files = [f.name for f in paths if f.stat().st_mtime > start_time]
                if file_to_listen in files:
                    array = np.load(self.share_path + "/" + file_to_listen)

                    # Write acknowledgement
                    self.append_file(f"{self.share_path}/{file_to_listen.replace('.npy', '')}-received", pi)

                    return array

                time.sleep(self.sleep_time)

            print(f"{self.node_type}: Timeout! No file was received from Laptop")
            return None

        else:
            print(f"{self.node_type}: Timeout! No file was sent or at least communicated that it was sent")
            return None
