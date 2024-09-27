from sys import argv

from isa import *
from json_utils import write_machine_code


def format_line(line: str) -> str:
    return line.strip().split(";")[0]


def parse_line(line: str) -> Opcode:
    return Opcode[line.upper()]


def parse_word(line: str) -> [Command]:
    line = line.split(": ")
    res: [Command] = []
    assert 2 == len(line), "Invalid data definition: invalid number of args"
    if line[1].startswith("0x"):
        res = [int(line[1][2:], 16)]
    else:
        line = line[1].split("'")
        assert len(line) == 3, "Invalid data definition: invalid number of args"
        if len(line[2]) == 0:
            res = [ord(ch) for ch in (line[1].strip('"') + "\0")]
        else:
            try:
                chars = line[1].strip("'") * int(line[2])
                res = [ord(ch) for ch in chars]
            except ValueError:
                raise ValueError("Size must be a integer")
    return res


def prepare_data(data: str):
    assert ".code" in data, "There is no code section"
    data = [format_line(str(line)) for line in data.splitlines()]
    data = [line.replace("\t", "") for line in data]
    data = "\n".join(data)
    return data


def translate_data(input_data: str) -> tuple[list[int], dict[str, int]]:
    code: list[int] = []
    labels: dict[str, int] = {}
    for line in input_data.splitlines():
        if line.split(" ")[0][-1] == ":":
            labels.update({line.split(" ")[0][:-1]: len(code)})
            code += parse_word(line)
        else:
            raise ValueError("Invalid data definition: missing ':'")
    return code, labels


def translate_code(input_data: str) -> [list[Command], dict[str, int]]:
    code: list[Command] = []
    labels: dict[str, int] = {}
    for line in input_data.splitlines():
        if line[-1] == ":":
            labels.update({line[:-1]: len(code)})
        elif line.count(" ") == 0:
            code.append(Command(parse_line(line)))
        elif line.startswith("push"):
            op, arg = line.split(" ", 2)
            code.append(Command(parse_line(op), arg))
    return code, labels


def translate_args(code: list[Command], labels: dict[str, int]) -> list[Command]:
    for i, command in enumerate(code):
        if command.code == Opcode.PUSH:
            assert code[i].arg in labels, f"None such label: {code[i].arg}"
            code[i].arg = labels[command.arg]
    return code


def translate(input_data: str) -> [list[Command], list[Command]]:
    input_str = prepare_data(input_data)
    data_section = input_str.split(".code\n")[0].strip(".data\n")
    code_section = input_str.split(".code\n")[1]
    data_section, labels = translate_data(data_section)
    code_section, code_labels = translate_code(code_section)
    labels.update(code_labels)
    code_section = translate_args(code_section, labels)
    return data_section, code_section


def main(source_file: str, data_file: str, code_file: str):
    with open(source_file, "r", encoding="utf-8") as file:
        input_data = file.read()
    data, code = translate(input_data)
    write_machine_code(data_file, data)
    write_machine_code(code_file, code)


if __name__ == "__main__":
    assert (len(argv) == 4), "Wrong number of arguments"
    _, source, data, code = argv
    main(source, data, code)
