from instruction import Instruction, \
    SEI, CLC, SEC, CLI, CLV, CLD, SED
from rom import ROM
from ppu import PPU
from status import Status
from ram import RAM
from memory import MemoryOwnerMixin

ZERO_BYTES = bytes.fromhex('00')


class CPU(object):
    # InstructionModes indicates the addressing mode for each instruction
    instructionModes = [
        6, 7, 6, 7, 11, 11, 11, 11, 6, 5, 4, 5, 1, 1, 1, 1,
        10, 9, 6, 9, 12, 12, 12, 12, 6, 3, 6, 3, 2, 2, 2, 2,
        1, 7, 6, 7, 11, 11, 11, 11, 6, 5, 4, 5, 1, 1, 1, 1,
        10, 9, 6, 9, 12, 12, 12, 12, 6, 3, 6, 3, 2, 2, 2, 2,
        6, 7, 6, 7, 11, 11, 11, 11, 6, 5, 4, 5, 1, 1, 1, 1,
        10, 9, 6, 9, 12, 12, 12, 12, 6, 3, 6, 3, 2, 2, 2, 2,
        6, 7, 6, 7, 11, 11, 11, 11, 6, 5, 4, 5, 8, 1, 1, 1,
        10, 9, 6, 9, 12, 12, 12, 12, 6, 3, 6, 3, 2, 2, 2, 2,
        5, 7, 5, 7, 11, 11, 11, 11, 6, 5, 6, 5, 1, 1, 1, 1,
        10, 9, 6, 9, 12, 12, 13, 13, 6, 3, 6, 3, 2, 2, 3, 3,
        5, 7, 5, 7, 11, 11, 11, 11, 6, 5, 6, 5, 1, 1, 1, 1,
        10, 9, 6, 9, 12, 12, 13, 13, 6, 3, 6, 3, 2, 2, 3, 3,
        5, 7, 5, 7, 11, 11, 11, 11, 6, 5, 6, 5, 1, 1, 1, 1,
        10, 9, 6, 9, 12, 12, 12, 12, 6, 3, 6, 3, 2, 2, 2, 2,
        5, 7, 5, 7, 11, 11, 11, 11, 6, 5, 6, 5, 1, 1, 1, 1,
        10, 9, 6, 9, 12, 12, 12, 12, 6, 3, 6, 3, 2, 2, 2, 2,
    ]

    # instructionSizes indicates the size of each instruction in bytes
    instructionSizes = [
        2, 2, 0, 0, 2, 2, 2, 0, 1, 2, 1, 0, 3, 3, 3, 0,
        2, 2, 0, 0, 2, 2, 2, 0, 1, 3, 1, 0, 3, 3, 3, 0,
        3, 2, 0, 0, 2, 2, 2, 0, 1, 2, 1, 0, 3, 3, 3, 0,
        2, 2, 0, 0, 2, 2, 2, 0, 1, 3, 1, 0, 3, 3, 3, 0,
        1, 2, 0, 0, 2, 2, 2, 0, 1, 2, 1, 0, 3, 3, 3, 0,
        2, 2, 0, 0, 2, 2, 2, 0, 1, 3, 1, 0, 3, 3, 3, 0,
        1, 2, 0, 0, 2, 2, 2, 0, 1, 2, 1, 0, 3, 3, 3, 0,
        2, 2, 0, 0, 2, 2, 2, 0, 1, 3, 1, 0, 3, 3, 3, 0,
        2, 2, 0, 0, 2, 2, 2, 0, 1, 0, 1, 0, 3, 3, 3, 0,
        2, 2, 0, 0, 2, 2, 2, 0, 1, 3, 1, 0, 0, 3, 0, 0,
        2, 2, 2, 0, 2, 2, 2, 0, 1, 2, 1, 0, 3, 3, 3, 0,
        2, 2, 0, 0, 2, 2, 2, 0, 1, 3, 1, 0, 3, 3, 3, 0,
        2, 2, 0, 0, 2, 2, 2, 0, 1, 2, 1, 0, 3, 3, 3, 0,
        2, 2, 0, 0, 2, 2, 2, 0, 1, 3, 1, 0, 3, 3, 3, 0,
        2, 2, 0, 0, 2, 2, 2, 0, 1, 2, 1, 0, 3, 3, 3, 0,
        2, 2, 0, 0, 2, 2, 2, 0, 1, 3, 1, 0, 3, 3, 3, 0,
    ]

    # instructionCycles indicates the number of cycles used by each instruction,
    # not including conditional cycles
    instructionCycles = [
        7, 6, 2, 8, 3, 3, 5, 5, 3, 2, 2, 2, 4, 4, 6, 6,
        2, 5, 2, 8, 4, 4, 6, 6, 2, 4, 2, 7, 4, 4, 7, 7,
        6, 6, 2, 8, 3, 3, 5, 5, 4, 2, 2, 2, 4, 4, 6, 6,
        2, 5, 2, 8, 4, 4, 6, 6, 2, 4, 2, 7, 4, 4, 7, 7,
        6, 6, 2, 8, 3, 3, 5, 5, 3, 2, 2, 2, 3, 4, 6, 6,
        2, 5, 2, 8, 4, 4, 6, 6, 2, 4, 2, 7, 4, 4, 7, 7,
        6, 6, 2, 8, 3, 3, 5, 5, 4, 2, 2, 2, 5, 4, 6, 6,
        2, 5, 2, 8, 4, 4, 6, 6, 2, 4, 2, 7, 4, 4, 7, 7,
        2, 6, 2, 6, 3, 3, 3, 3, 2, 2, 2, 2, 4, 4, 4, 4,
        2, 6, 2, 6, 4, 4, 4, 4, 2, 5, 2, 5, 5, 5, 5, 5,
        2, 6, 2, 6, 3, 3, 3, 3, 2, 2, 2, 2, 4, 4, 4, 4,
        2, 5, 2, 5, 4, 4, 4, 4, 2, 4, 2, 4, 4, 4, 4, 4,
        2, 6, 2, 8, 3, 3, 5, 5, 2, 2, 2, 2, 4, 4, 6, 6,
        2, 5, 2, 8, 4, 4, 6, 6, 2, 4, 2, 7, 4, 4, 7, 7,
        2, 6, 2, 8, 3, 3, 5, 5, 2, 2, 2, 2, 4, 4, 6, 6,
        2, 5, 2, 8, 4, 4, 6, 6, 2, 4, 2, 7, 4, 4, 7, 7,
    ]

    # instructionPageCycles indicates the number of cycles used by each instruction
    # when a page is crossed
    instructionPageCycles = [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0,
    ]

    # instructionNames indicates the name of each instruction
    # Just the instructions in matrix for the 6502 instruction set
    # https://en.wikipedia.org/wiki/MOS_Technology_6502#Assembly_language_instructions
    instructionNames = [
        "BRK", "ORA", "KIL", "SLO", "NOP", "ORA", "ASL", "SLO",
        "PHP", "ORA", "ASL", "ANC", "NOP", "ORA", "ASL", "SLO",
        "BPL", "ORA", "KIL", "SLO", "NOP", "ORA", "ASL", "SLO",
        CLC, "ORA", "NOP", "SLO", "NOP", "ORA", "ASL", "SLO",
        "JSR", "AND", "KIL", "RLA", "BIT", "AND", "ROL", "RLA",
        "PLP", "AND", "ROL", "ANC", "BIT", "AND", "ROL", "RLA",
        "BMI", "AND", "KIL", "RLA", "NOP", "AND", "ROL", "RLA",
        SEC, "AND", "NOP", "RLA", "NOP", "AND", "ROL", "RLA",
        "RTI", "EOR", "KIL", "SRE", "NOP", "EOR", "LSR", "SRE",
        "PHA", "EOR", "LSR", "ALR", "JMP", "EOR", "LSR", "SRE",
        "BVC", "EOR", "KIL", "SRE", "NOP", "EOR", "LSR", "SRE",
        CLI, "EOR", "NOP", "SRE", "NOP", "EOR", "LSR", "SRE",
        "RTS", "ADC", "KIL", "RRA", "NOP", "ADC", "ROR", "RRA",
        "PLA", "ADC", "ROR", "ARR", "JMP", "ADC", "ROR", "RRA",
        "BVS", "ADC", "KIL", "RRA", "NOP", "ADC", "ROR", "RRA",
        SEI, "ADC", "NOP", "RRA", "NOP", "ADC", "ROR", "RRA",
        "NOP", "STA", "NOP", "SAX", "STY", "STA", "STX", "SAX",
        "DEY", "NOP", "TXA", "XAA", "STY", "STA", "STX", "SAX",
        "BCC", "STA", "KIL", "AHX", "STY", "STA", "STX", "SAX",
        "TYA", "STA", "TXS", "TAS", "SHY", "STA", "SHX", "AHX",
        "LDY", "LDA", "LDX", "LAX", "LDY", "LDA", "LDX", "LAX",
        "TAY", "LDA", "TAX", "LAX", "LDY", "LDA", "LDX", "LAX",
        "BCS", "LDA", "KIL", "LAX", "LDY", "LDA", "LDX", "LAX",
        CLV, "LDA", "TSX", "LAS", "LDY", "LDA", "LDX", "LAX",
        "CPY", "CMP", "NOP", "DCP", "CPY", "CMP", "DEC", "DCP",
        "INY", "CMP", "DEX", "AXS", "CPY", "CMP", "DEC", "DCP",
        "BNE", "CMP", "KIL", "DCP", "NOP", "CMP", "DEC", "DCP",
        CLD, "CMP", "NOP", "DCP", "NOP", "CMP", "DEC", "DCP",
        "CPX", "SBC", "NOP", "ISC", "CPX", "SBC", "INC", "ISC",
        "INX", "SBC", "NOP", "SBC", "CPX", "SBC", "INC", "ISC",
        "BEQ", "SBC", "KIL", "ISC", "NOP", "SBC", "INC", "ISC",
        SED, "SBC", "NOP", "ISC", "NOP", "SBC", "INC", "ISC",
    ]

    def __init__(self, ram: RAM, ppu: PPU):

        self.ram = ram
        self.ppu = ppu

        # Memory Owners
        self.memory_owners = [  # type: List[MemoryOwnerMixin]
            self.ram,
            self.ppu
        ]

        # Counter registers
        self.pc_reg = None  # type: int
        self.sp_reg = None

        # Status registers
        self.p_reg = None  # type: Status

        # Data registers
        self.x_reg = None  # type: bytes
        self.y_reg = None  # type: bytes
        self.a_reg = None  # type: bytes

        self.rom = None
        self.running = True

        self.address = 0
        self.page_crossed = False
        self.cycles = 0

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
        self.a_reg = '00'
        self.x_reg = '00'
        self.y_reg = '00'

        self.sp_reg = 'FD'

        # TODO: IMPLEMENTAR LA MEMORIA RAM!!! FALTA MANDAR A CERO
        # TODO: CIERTOS LUGARES DE LA MEMORIA

    def read16(self):
        lo = self.rom.get(self.address + 1)
        hi = self.rom.get(self.address + 2)
        return int.from_bytes(lo + hi, byteorder='little')

    # emulates a 6502 bug read
    def read16bug(self, address: int):
        a = address
        b = (a & 0xFF00) | int.from_bytes(bytes([a]), byteorder='little') + 1
        lo = self.rom.get(a)
        hi = self.rom.get(b)
        return int.from_bytes(lo + hi, byteorder='little')

    # pagesDiffer returns true if the two addresses reference different pages
    @staticmethod
    def pages_differ(a: bytes, b: bytes) -> bool:
        return (a & 0xFF00) != (b & 0xFF00)

    def mode_absolute(self):
        self.address = self.read16()

    def mode_absolute_x(self):
        self.address = self.read16() + int.from_bytes(bytes.fromhex(self.x_reg), byteorder='little')
        self.page_crossed = self.pages_differ(self.address - int.from_bytes(bytes.fromhex(self.x_reg), byteorder='little'), self.address)

    def mode_absolute_y(self):
        self.address = self.read16() + int.from_bytes(bytes.fromhex(self.y_reg), byteorder='little')
        self.page_crossed = self.pages_differ(self.address - int.from_bytes(bytes.fromhex(self.y_reg), byteorder='little'), self.address)

    def mode_accumulator(self):
        self.address = 0

    def mode_immediate(self):
        self.address = self.pc_reg + 1

    def mode_implied(self):
        self.address = 0

    def mode_indexed_indirect(self):
        self.address = self.read16bug(self.pc_reg + 1 + int.from_bytes(bytes.fromhex(self.x_reg), byteorder='little'))

    def mode_indirect(self):
        self.address = self.read16bug(self.pc_reg + 1)

    def mode_indirect_indexed(self):
        self.address = self.read16bug(self.pc_reg + 1 + int.from_bytes(bytes.fromhex(self.y_reg), byteorder='little'))
        self.page_crossed = self.pages_differ(self.address - int.from_bytes(bytes.fromhex(self.y_reg), byteorder='little'), self.address)

    def mode_relative(self):
        offset = self.pc_reg + 1
        if offset < 0x80:
            self.address = self.pc_reg + 2 + offset
        else:
            self.address = self.pc_reg + 2 + offset - 0x100

    def mode_zero_page(self):
        self.address = self.pc_reg + 1

    def mode_zero_page_x(self):
        self.address = (self.pc_reg + 1 + int.from_bytes(bytes.fromhex(self.x_reg), byteorder='little')) & 0xff

    def mode_zero_page_y(self):
        self.address = (self.pc_reg + 1 + int.from_bytes(bytes.fromhex(self.y_reg), byteorder='little')) & 0xff

    def addressing_modes(self, mode: int):
        switcher = {
            1: self.mode_absolute(),
            2: self.mode_absolute_x(),
            3: self.mode_absolute_y(),
            4: self.mode_accumulator(),
            5: self.mode_immediate(),
            6: self.mode_implied(),
            7: self.mode_indexed_indirect(),
            8: self.mode_indirect(),
            9: self.mode_indirect_indexed(),
            10: self.mode_relative(),
            11: self.mode_zero_page(),
            12: self.mode_zero_page_x(),
            13: self.mode_zero_page_y()
        }
        switcher.get(mode, lambda: "Invalid mode")

    def run_rom(self, rom: ROM):
        # Load rom
        self.rom = rom
        self.pc_reg = rom.header_size

        while self.running:
            identifier_byte = rom.get(self.pc_reg)

            op_code = rom.get(self.pc_reg)
            op_position = int.from_bytes(op_code, byteorder='little')
            mode = self.instructionModes[op_position]

            print("Mode: ")
            print(mode)
            print(op_code)

            self.addressing_modes(mode)

            self.pc_reg += self.instructionSizes[op_position]
            print(self.pc_reg)
            self.cycles += self.instructionCycles[op_position]

            if self.page_crossed:
                self.cycles += self.instructionPageCycles[op_position]

            instruction_class = self.instructionNames[op_position]

            instruction = instruction_class()
            print(instruction)
            instruction.execute(self)
