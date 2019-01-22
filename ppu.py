from typing import List
from memory import MemoryOwnerMixin

PPU_SIZE = 8  # 8B internal VRAM


class PPU(MemoryOwnerMixin, object):
    memory_start_location = int.from_bytes(bytes.fromhex('2000'), byteorder='big')
    memory_end_location = int.from_bytes(bytes.fromhex('2007'), byteorder='big')

    def __init__(self):
        self.memory = [0 for _ in range(PPU_SIZE)],  # type: List[bytes]

    def get_memory(self) -> List[bytes]:
        return self.memory
