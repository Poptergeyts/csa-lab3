from alu import ALU, ALUCommands, ALUMux
from constants import *
from io_controller import IO
from isa import Command


class DataPath:
    pc: int = 0
    ar: int = 0

    def __init__(self, alu: ALU, program: list[Command], data: list[int], mem: dict[int, IO]):
        self.command_memory = program + [0] * (MEMORY_SIZE - len(program))
        self.data_memory = data + [0] * (MEMORY_SIZE - len(data))
        self.stack: list[int] = []
        self.mem = mem
        self.alu = alu

    def signal_pop(self):
        self.stack.pop()

    def signal_load_command(self) -> Command:
        return self.command_memory[self.pc]

    def signal_push(self, value: int):
        self.stack.append(value)

    def signal_write_first(self, value: int):
        self.stack[-1] = value

    def signal_write_second(self, value: int):
        self.stack[-2] = value

    def signal_ld(self) -> int:
        if self.ar in self.mem:
            return self.mem[self.ar].read_byte()
        value = self.data_memory[self.ar]
        return value

    def signal_st(self, value: int):
        if self.ar in self.mem:
            self.mem[self.ar].write_byte(value)
            return
        self.data_memory[self.ar] = value

    def set_ar(self, value: int):
        self.ar = value

    def set_pc(self, value: int):
        self.pc = value

    def perform_alu_operation(self, left: ALUMux, right: ALUMux, alu_operation: ALUCommands) -> int:
        left = self.get_first() if left == ALUMux.TOP else 0
        right = self.get_second() if right == ALUMux.TOP else 0
        return self.alu.perform(left, right, alu_operation)

    def get_first(self):
        return self.stack[-1]

    def get_second(self):
        return self.stack[-2]
