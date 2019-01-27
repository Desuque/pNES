from typing import List
from memory import MemoryOwnerMixin

PPU_SIZE = 8  # 8B internal VRAM


class PPU(MemoryOwnerMixin, object):
    memory_start_location = 0x2000
    memory_end_location = 0x2007

    def __init__(self):
        self.memory = list([0 for _ in range(PPU_SIZE)])  # type: List[int]

    def get_memory(self) -> List[int]:
        return self.memory
