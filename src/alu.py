from enum import Enum


class ALUCommands(Enum):
    MUL = "mul"
    DIV = "div"
    ADD = "add"
    SUB = "sub"
    XOR = "xor"
    INC = "inc"


class ALUMux(Enum):
    TOP = "top"
    NONE = "none"


class ALU:
    _z_flag: bool

    def __init__(self):
        self._z_flag = False

    @property
    def z_flag(self):
        return self._z_flag

    def perform(self, left: int, right: int, command: ALUCommands) -> int:
        output_value: int
        if command == ALUCommands.SUB:
            output_value = left - right
        elif command == ALUCommands.INC:
            output_value = left + 1
        elif command == ALUCommands.DIV:
            output_value = left // right
        elif command == ALUCommands.XOR:
            output_value = left ^ right
        elif command == ALUCommands.ADD:
            output_value = left + right
        elif command == ALUCommands.MUL:
            output_value = left * right
        else:
            raise NotImplementedError("Invalid ALU command")
        self._z_flag = output_value == 0
        return output_value
