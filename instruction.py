# Que se acaben los vivos, los idiotas, el hambre, o esta politica, que es mas o menos lo mismo y ya no da para mas
from abc import ABC, abstractmethod


class Instruction(ABC):

    @abstractmethod
    def execute(self, cpu):
        pass


class BPL(Instruction):
    def execute(self, cpu):
        if cpu.p_reg.negative_bit == 0:
            cpu.pc_reg = cpu.address
            cpu.add_branch_cycle()


class LDX(Instruction):
    def execute(self, cpu):
        cpu.x_reg = cpu.read(cpu.address)
        cpu.set_z(cpu.x_reg)
        cpu.set_n(cpu.x_reg)


class TXS(Instruction):
    def execute(self, cpu):
        cpu.sp_reg = cpu.x_reg


class LDA(Instruction):
    def execute(self, cpu):
        cpu.a_reg = cpu.read(cpu.address)
        cpu.set_z(cpu.a_reg)
        cpu.set_n(cpu.a_reg)


class STA(Instruction):
    def execute(self, cpu):
        memory_address = int.from_bytes(cpu.read(cpu.address), byteorder='little')
        value_to_store = int.from_bytes(cpu.a_reg, byteorder='little')

        memory_owner = cpu.get_memory_owner(memory_address)
        memory_owner.set(memory_address, value_to_store)

        print(cpu.ram.memory[0])

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


class CLC(Instruction):
    def execute(self, cpu):
        cpu.p_reg.carry_bit = False


class SEC(Instruction):
    def execute(self, cpu):
        cpu.p_reg.carry_bit = True


class CLI(Instruction):
    def execute(self, cpu):
        cpu.p_reg.interrupt_bit = False


class SEI(Instruction):
    def execute(self, cpu):
        cpu.p_reg.interrupt_bit = True


class CLV(Instruction):
    def execute(self, cpu):
        cpu.p_reg.overflow_bit = False


class CLD(Instruction):
    def execute(self, cpu):
        cpu.p_reg.decimal_bit = False


class SED(Instruction):
    def execute(self, cpu):
        cpu.p_reg.decimal_bit = True

# Illegal opcodes


class AHX(Instruction):
    def execute(self, cpu):
        print("Illegal opcode: {}".format(self.__class__.__name__))


class ALR(Instruction):
    def execute(self, cpu):
        print("Illegal opcode: {}".format(self.__class__.__name__))


class ANC(Instruction):
    def execute(self, cpu):
        print("Illegal opcode: {}".format(self.__class__.__name__))


class ARR(Instruction):
    def execute(self, cpu):
        print("Illegal opcode: {}".format(self.__class__.__name__))


class AXS(Instruction):
    def execute(self, cpu):
        print("Illegal opcode: {}".format(self.__class__.__name__))


class DCP(Instruction):
    def execute(self, cpu):
        print("Illegal opcode: {}".format(self.__class__.__name__))


class ISC(Instruction):
    def execute(self, cpu):
        print("Illegal opcode: {}".format(self.__class__.__name__))


class KIL(Instruction):
    def execute(self, cpu):
        print("Illegal opcode: {}".format(self.__class__.__name__))


class LAS(Instruction):
    def execute(self, cpu):
        print("Illegal opcode: {}".format(self.__class__.__name__))


class LAX(Instruction):
    def execute(self, cpu):
        print("Illegal opcode: {}".format(self.__class__.__name__))


class RLA(Instruction):
    def execute(self, cpu):
        print("Illegal opcode: {}".format(self.__class__.__name__))


class RRA(Instruction):
    def execute(self, cpu):
        print("Illegal opcode: {}".format(self.__class__.__name__))


class SAX(Instruction):
    def execute(self, cpu):
        print("Illegal opcode: {}".format(self.__class__.__name__))


class SHX(Instruction):
    def execute(self, cpu):
        print("Illegal opcode: {}".format(self.__class__.__name__))


class SHY(Instruction):
    def execute(self, cpu):
        print("Illegal opcode: {}".format(self.__class__.__name__))


class SLO(Instruction):
    def execute(self, cpu):
        print("Illegal opcode: {}".format(self.__class__.__name__))


class SRE(Instruction):
    def execute(self, cpu):
        print("Illegal opcode: {}".format(self.__class__.__name__))


class TAS(Instruction):
    def execute(self, cpu):
        print("Illegal opcode: {}".format(self.__class__.__name__))


class XAA(Instruction):
    def execute(self, cpu):
        print("Illegal opcode: {}".format(self.__class__.__name__))
