from abc import ABC, abstractmethod


class Instruction(ABC):

    @abstractmethod
    def execute(self, cpu):
        pass


# ADC (ADd with Carry)

class ADCInmInstruction(Instruction):
    adc_inst = [
"""
Affects Flags: S V Z C

MODE           SYNTAX       HEX LEN TIM
Immediate     ADC #$44      $69  2   2
Zero Page     ADC $44       $65  2   3
Zero Page,X   ADC $44,X     $75  2   4
Absolute      ADC $4400     $6D  3   4
Absolute,X    ADC $4400,X   $7D  3   4+
Absolute,Y    ADC $4400,Y   $79  3   4+
Indirect,X    ADC ($44,X)   $61  2   6
Indirect,Y    ADC ($44),Y   $71  2   5+

+ add 1 cycle if page boundary crossed
"""
    ]

    # TODO: Instruction length
    def execute(self, cpu):
        # TODO: Overflow in bit 7, to code carry flag
        if cpu.a_reg_is_zero():
            cpu.p_reg.zero_bit = True

        # TODO: Overflow flag, negative flag


class LDAInmInstruction(Instruction):
    instruction_length = 2

    def execute(self, cpu):
        cpu.a_reg = cpu.address

        if cpu.a_reg_is_zero():
            cpu.p_reg.zero_bit = True

        if cpu.a_reg_is_negative():
            cpu.p_reg.negative_bit = True


class STAAbsInstruction(Instruction):

    def execute(self, cpu):
        memory_address = int.from_bytes(cpu.address, byteorder='little')
        value_to_store = cpu.a_reg

        memory_owner = cpu.get_memory_owner(memory_address)
        memory_owner.set(memory_address, value_to_store)

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
