from abc import ABC, abstractmethod

import struct


class Instruction(ABC):
    def __init__(self, identifier_byte: bytes):
        self.identifier_byte = identifier_byte

    @property
    def instruction_length(self):
        return 1

    @abstractmethod
    def execute(self):
        print('Identifier byte: ', self.identifier_byte)
        pass


# Status instructions

class ADCInstruction(Instruction):
    # TODO: Instruction length
    def execute(self, cpu, data_bytes):
        # TODO: Overflow in bit 7, to code carry flag
        if cpu.a_reg_is_zero():
            cpu.p_reg.zero_bit = True

        # TODO: Overflow flag, negative flag


class LDAInmInstruction(Instruction):
    instruction_length = 2

    def execute(self, cpu, data_bytes):
        cpu.a_reg = data_bytes[0]

        if cpu.a_reg_is_zero():
            cpu.p_reg.zero_bit = True

        if cpu.a_reg_is_negative():
            cpu.p_reg.negative_bit = True


class STAAbsInstruction(Instruction):
    instruction_length = 3

    def execute(self, cpu, data_bytes):
        memory_address = int.from_bytes(data_bytes, byteorder='little')
        value_to_store = cpu.a_reg

        memory_owner = cpu.get_memory_owner(memory_address)
        memory_owner.set_bytes(memory_address, value_to_store)

        print(memory_address)

# Status instructions
"""
These instructions are implied mode, have a length of one byte and require two machine cycles.

MNEMONIC                       HEX
CLC (CLear Carry)              $18
SEC (SEt Carry)                $38
CLI (CLear Interrupt)          $58
SEI (SEt Interrupt)            $78
CLV (CLear oVerflow)           $B8
CLD (CLear Decimal)            $D8
SED (SEt Decimal)              $F8
"""


class CLCInstruction(Instruction):
    instruction_length = 1

    def execute(self, cpu, data_bytes):
        cpu.p_reg.carry_bit = False


class SECInstruction(Instruction):
    instruction_length = 1

    def execute(self, cpu, data_bytes):
        cpu.p_reg.carry_bit = True


class CLIInstruction(Instruction):
    instruction_length = 1

    def execute(self, cpu, data_bytes):
        cpu.p_reg.interrupt_bit = False


class SEIInstruction(Instruction):
    instruction_length = 1

    def execute(self, cpu, data_bytes):
        cpu.p_reg.interrupt_bit = True


class CLVInstruction(Instruction):
    instruction_length = 1

    def execute(self, cpu, data_bytes):
        cpu.p_reg.overflow_bit = False


class CLDInstruction(Instruction):
    instruction_length = 1

    def execute(self, cpu, data_bytes):
        cpu.p_reg.decimal_bit = False


class SEDInstruction(Instruction):
    instruction_length = 1

    def execute(self, cpu, data_bytes):
        cpu.p_reg.decimal_bit = True
