from typing import List
from memory import MemoryOwnerMixin

RAM_SIZE = 2048  # 2KB internal RAM


class RAM(MemoryOwnerMixin, object):
    memory_start_location = int.from_bytes(bytes.fromhex('0000'), byteorder='big')
    memory_end_location = int.from_bytes(bytes.fromhex('1FFF'), byteorder='big')

    def __init__(self):
        self.memory = [0 for _ in range(RAM_SIZE)],  # type: List[bytes]

    def get_memory(self) -> List[bytes]:
        return self.memory
