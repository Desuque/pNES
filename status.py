"""
7  bit  0
---- ----
NVss DIZC
|||| ||||
|||| |||+- Carry
|||| ||+-- Zero
|||| |+--- Interrupt Disable
|||| +---- Decimal
||++------ No CPU effect, see: the B flag
|+-------- Overflow
+--------- Negative

https://wiki.nesdev.com/w/index.php/Status_flags
"""


class Status(object):
    def __init__(self):
        #  P = 0011 0100 ($34)
        #  P = NVss DIZC
        self.carry_bit = False  # type: bool
        self.zero_bit = False  # type: bool
        self.interrupt_bit = True  # type: bool
        self.decimal_bit = False  # type: bool
        self.no_effect_four_bit = True  # type: bool
        self.no_effect_five_bit = True  # type: bool
        self.overflow_bit = False  # type: bool
        self.negative_bit = False  # type: bool
