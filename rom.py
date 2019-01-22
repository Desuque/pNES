from memory import MemoryOwnerMixin
from typing import List

KB = 1024

'''
0 - 3: Constant $4E $45 $53 $1A("NES" followed by MS-DOS end-of-file)
4: Size of PRG ROM in 16 KB units
5: Size of CHR ROM in 8 KB units(Value 0 means the board uses CHR RAM)
6: Flags 6 - Mapper, mirroring, battery, trainer
7: Flags 7 - Mapper, VS / Playchoice, NESv2.0
8: Flags 8 - PRG - RAM size(rarely used extension)
9: Flags 9 - TV system(rarely used extension)
10: Flags 10 - TV system, PRG - RAM presence(unofficial, rarely used extension)
11 - 15: Unused padding(should be filled with zero, but some rippers put their name across bytes 7-15)
'''


class ROM(MemoryOwnerMixin, object):

    def __init__(self, rom_bytes: bytes):
        # Flag trainer is the second bit
        self.flag_trainer = rom_bytes[6] >> 2 & 1
        self.size_pgr_rom = rom_bytes[4]
        self.rom_bytes = rom_bytes

        # TODO: Suponer que trainer no es cero
        if self.flag_trainer is 0:
            self.header_size = 16
            self.prg_bytes = rom_bytes[self.header_size: self.header_size + 16 * KB * self.size_pgr_rom]
        else:
            raise Exception('NOT IMPLEMENTED FLAG TRAINER')

    def get_memory(self) -> List[bytes]:
        return self.rom_bytes

    def set_bytes(self, position, value):
        raise Exception('Trying to write in Read Only Memory')
