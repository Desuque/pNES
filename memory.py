from abc import abstractmethod, ABC
from typing import List


class MemoryOwnerMixin(ABC):
    @property
    def memory_start_location(self) -> int:
        pass

    @property
    def memory_end_location(self) -> int:
        pass

    @abstractmethod
    def get_memory(self) -> List[bytes]:
        pass

    def get(self, position: int) -> str:
            return self.get_memory()[position - self.memory_start_location]

    def set(self, position, value: bytes):
        self.get_memory()[position - self.memory_start_location] = value
