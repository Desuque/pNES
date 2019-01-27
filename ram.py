from typing import List
from memory import MemoryOwnerMixin

RAM_SIZE = 2048  # 2KB internal RAM


class RAM(MemoryOwnerMixin, object):
    memory_start_location = 0x0000
    memory_end_location = 0x1FFF

    def __init__(self):
        self.memory = list([0 for _ in range(RAM_SIZE)])  # type: List[int]

    def get_memory(self) -> List[int]:
        return self.memory
