from instruction import Instruction, LDAInmInstruction, \
    SEIInstruction, CLDInstruction, STAAbsInstruction
from rom import ROM
from ppu import PPU
from status import Status
from ram import RAM
from memory import MemoryOwnerMixin

ZERO_BYTES = bytes.fromhex('00')


class CPU(object):
    def __init__(self, ram: RAM, ppu: PPU):

        self.ram = ram
        self.ppu = ppu

        # Memory Owners
        self.memory_owners = [  # type: List[MemoryOwnerMixin]
            self.ram,
            self.ppu
        ]

        # Counter registers
        self.pc_reg = None
        self.sp_reg = None

        # Status registers
        self.p_reg = None  # type: Status

        # Data registers
        self.x_reg = None
        self.y_reg = None
        self.a_reg = None  # type: bytes

        self.rom = None
        self.running = True

        # https://en.wikipedia.org/wiki/MOS_Technology_6502#Assembly_language_instructions
        self.instruction_mapping = {
            bytes.fromhex('78'): SEIInstruction,
            bytes.fromhex('D8'): CLDInstruction,
            bytes.fromhex('A9'): LDAInmInstruction,
            bytes.fromhex('8D'): STAAbsInstruction
        }

    def get_memory_owner(self, memory_position: int) -> MemoryOwnerMixin:
        if self.rom.memory_start_location <= memory_position <= self.rom.memory_end_location:
            return self.rom

        for owner in self.memory_owners:
            if owner.memory_start_location <= memory_position <= owner.memory_end_location:
                return owner

        raise Exception('Memory owner doesnt exists')

    def a_reg_is_zero(self):
        return self.a_reg == ZERO_BYTES

    def a_reg_is_negative(self):
        # TODO: DO IT
        return 1

    def process_instructions(self, instruction: Instruction):
        instruction.process()
        pass

    def start_up(self):
        #  Set initial values of registers
        #  https://wiki.nesdev.com/w/index.php/CPU_power_up_state
        #  SP = $FD

        self.p_reg = Status()
        self.a_reg = 0
        self.x_reg = 0
        self.y_reg = 0

        self.sp_reg = 0xFD

        # TODO: IMPLEMENTAR LA MEMORIA RAM!!! FALTA MANDAR A CERO
        # TODO: CIERTOS LUGARES DE LA MEMORIA

    def run_rom(self, rom: ROM):
        # Load rom
        self.rom = rom
        self.pc_reg = rom.header_size

        while self.running:
            # Get the current byte at pc
            identifier_byte = rom.get(self.pc_reg)

            # Turn the byte into a instruction
            instruction_class = self.instruction_mapping.get(identifier_byte, None)

            if instruction_class is None:
                raise Exception('The instruction {} doesnt exists'.format(identifier_byte))

            # We have a valid instruction class
            instruction = instruction_class(identifier_byte)

            # Get the correct amount of data bytes
            num_data_bytes = instruction.instruction_length - 1
            data_bytes = rom.get(self.pc_reg + 1, num_data_bytes)

            instruction.execute(self, data_bytes)

            self.pc_reg += instruction.instruction_length

