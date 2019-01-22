from abc import abstractmethod, ABC
from typing import List


class MemoryOwnerMixin(ABC):
    @property
    def memory_start_location(self):
        pass

    @property
    def memory_end_location(self):
        pass

    @abstractmethod
    def get_memory(self) -> List[bytes]:
        pass

    def get_bytes(self, position: int, size: int = 1) -> bytes:
            return self.get_memory()[position:position+size]

    def set_bytes(self, position, value: bytes):
        if value.__len__() > 1:
            raise Exception('Trying to store multiple bytes in memory')

        self.get_memory()[position] = value
