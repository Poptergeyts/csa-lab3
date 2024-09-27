from data_path import DataPath, ALUCommands, ALUMux
from isa import Opcode, Command


class ControlUnit:
    tick: int = 0

    def __init__(self, data_path: DataPath):
        self.data_path = data_path

    def next_tick(self):
        self.tick += 1

    def current_tick(self) -> int:
        return self.tick

    def initialize_datapath(self):
        self.data_path.set_pc(0)
        self.data_path.set_ar(0)

    def decode_and_execute_command(self):
        command = self.data_path.signal_load_command()
        self.next_tick()

        self.data_path.set_pc(self.data_path.pc + 1)
        self.next_tick()

        if command.code == Opcode.POP.value:
            self.execute_pop()
        elif command.code == Opcode.SWAP.value:
            self.execute_swap()
        elif command.code == Opcode.LD.value:
            self.execute_ld()
        elif command.code == Opcode.ST.value:
            self.execute_st()
        elif command.code == Opcode.INC.value:
            self.execute_single_operand_alu_operation(command)
        elif command.code in [
            Opcode.MUL.value,
            Opcode.DIV.value,
            Opcode.ADD.value,
            Opcode.SUB.value,
            Opcode.XOR.value
        ]:
            self.execute_double_operand_alu_operation(command)
        elif command.code == Opcode.JMP.value:
            self.execute_jmp()
        elif command.code == Opcode.JZ.value:
            self.execute_jz()
        elif command.code == Opcode.JNZ.value:
            self.execute_jnz()
        elif command.code == Opcode.PUSH.value:
            self.execute_push(command)
        elif command.code == Opcode.HLT.value:
            self.execute_hlt()
        elif command.code == Opcode.TEST.value:
            self.execute_test()
        else:
            raise NotImplementedError

    def execute_pop(self):
        self.data_path.signal_pop()
        self.next_tick()

    def execute_swap(self):
        self.data_path.signal_write_first(
            self.data_path.perform_alu_operation(ALUMux.TOP, ALUMux.TOP, ALUCommands.XOR))
        self.next_tick()

        self.data_path.signal_write_second(
            self.data_path.perform_alu_operation(ALUMux.TOP, ALUMux.TOP, ALUCommands.XOR))
        self.next_tick()

        self.data_path.signal_write_first(
            self.data_path.perform_alu_operation(ALUMux.TOP, ALUMux.TOP, ALUCommands.XOR))
        self.next_tick()

    def execute_ld(self):
        self.data_path.set_ar(
            self.data_path.perform_alu_operation(ALUMux.TOP, ALUMux.NONE, ALUCommands.ADD))
        self.next_tick()

        self.data_path.signal_push(self.data_path.signal_ld())
        self.next_tick()

    def execute_st(self):
        self.data_path.set_ar(
            self.data_path.perform_alu_operation(ALUMux.TOP, ALUMux.NONE, ALUCommands.ADD))
        self.next_tick()
        self.execute_swap()

        self.data_path.signal_st(
            self.data_path.perform_alu_operation(ALUMux.TOP, ALUMux.NONE, ALUCommands.ADD))
        self.next_tick()

        self.data_path.signal_pop()
        self.next_tick()

    def execute_single_operand_alu_operation(self, command: Command):
        self.data_path.signal_write_first(
            self.data_path.perform_alu_operation(
                ALUMux.TOP, ALUMux.NONE, ALUCommands[command.code.upper()]))
        self.next_tick()

    def execute_double_operand_alu_operation(self, command: Command):
        self.data_path.signal_write_second(
            self.data_path.perform_alu_operation(
                ALUMux.TOP, ALUMux.TOP, ALUCommands[command.code.upper()]))
        self.next_tick()
        self.data_path.signal_pop()
        self.next_tick()

    def execute_jmp(self):
        self.data_path.set_pc(
            self.data_path.perform_alu_operation(ALUMux.TOP, ALUMux.NONE, ALUCommands.ADD))
        self.next_tick()
        self.data_path.signal_pop()
        self.next_tick()

    def execute_jnz(self):
        if self.data_path.alu.z_flag != 1:
            self.execute_jmp()
        else:
            self.data_path.signal_pop()
            self.next_tick()

    def execute_jz(self):
        if self.data_path.alu.z_flag == 1:
            self.execute_jmp()
        else:
            self.data_path.signal_pop()
            self.next_tick()

    def execute_push(self, command: Command):
        assert command.arg is not None and isinstance(command.arg, int), "Invalid PUSH arg"
        self.data_path.signal_push(command.arg)
        self.next_tick()

    def execute_hlt(self):
        raise StopIteration

    def execute_test(self):
        self.data_path.perform_alu_operation(ALUMux.TOP, ALUMux.NONE, ALUCommands.XOR)
        self.next_tick()

    def __str__(self):
        state_repr = (
            f"TICK: {self.current_tick():4} "
            f"PC: {self.data_path.pc:3} "
            f"AR: {self.data_path.ar:4} "
            f"Z_FLAG: {self.data_path.alu.z_flag:1} "
        )
        stack_repr = f"STACK: {self.data_path.stack}"
        command_repr = "COMMAND: " + str(self.data_path.command_memory[self.data_path.pc])
        data_repr = "DATA: " + str(self.data_path.data_memory[self.data_path.ar])

        return f"{state_repr} {command_repr:40} {data_repr:12} {stack_repr}"
