import argparse
import logging

from control_unit import ControlUnit
from data_path import ALU, IO, DataPath
from isa import Command
from json_utils import read_machine_code


def execute(code: dict, data: [int], input_data) -> [str, int, int]:
    alu = ALU()
    io = IO(input_data)
    ios = {2 ** 10 - 1: io}
    code = [Command.from_dict(c) for c in code]
    data_path = DataPath(alu, code, data, ios)
    control_unit = ControlUnit(data_path)
    control_unit.initialize_datapath()
    instr_counter = 0
    logging.debug("%s", control_unit)
    try:
        while True:
            control_unit.decode_and_execute_command()
            instr_counter += 1
            logging.debug("%s", control_unit)
    except StopIteration:
        instr_counter += 1
    return io.output, instr_counter, control_unit.current_tick()


def main(code_filename: str, data_filename: str, input_filename: str):
    code = read_machine_code(code_filename)
    data = read_machine_code(data_filename)
    with open(input_filename, encoding="utf-8") as file:
        input_text = file.read()
        input_data = list(ord(c) for c in (input_text + "\0"))

    output, instr_counter, ticks = execute(code, data, input_data)
    print("output: ", "".join(output))
    print("command_counter: ", instr_counter, " number_of_ticks: ", ticks)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    logging.basicConfig(format='%(message)s')
    parser = argparse.ArgumentParser()
    parser.add_argument("code_file", type=str, nargs=1)
    parser.add_argument("data_file", type=str, nargs=1)
    parser.add_argument("io_file", type=str, nargs=1)
    args = parser.parse_args()
    main(args.code_file[0], args.data_file[0], args.io_file[0])
