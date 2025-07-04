import time
import numpy as np
from abc import ABC, abstractmethod

class ICTransport(ABC):
    def __init__(self,
                 share_path: str = "./ic-transport", # Please always provide absolute full path
                 sync_file: str = "./synchroniser.log", # Please always provide absolute full path
                 timeout_s: float = 1,
                 sleep_time: float = 1):
        
        self.share_path = share_path
        self.sync_file = sync_file

        self.timeout_s = timeout_s
        self.sleep_time = sleep_time

    def not_timeout(self, start_time, timeout_s):
        if timeout_s:
            return (time.time() - start_time < timeout_s)
        else:
            return True

    @abstractmethod    
    def append_file(self, string):
        pass
    
    @abstractmethod
    def read_last(self):
        pass

    @abstractmethod
    def clear_sync(self, sync_file):
        pass

    @abstractmethod
    def await_sending(self, start_time, timeout_s=None) -> bool:
        pass

    @abstractmethod
    def send(self, n: np.array) -> bool:
        pass

    @abstractmethod
    def listen(self, timeout_s=None) -> np.array:
        pass