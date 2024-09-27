import json
from enum import Enum

from isa import Command


class CustomEncoder(json.JSONEncoder):
    def default(self, arg):
        if isinstance(arg, Command):
            return arg.to_dict()
        if isinstance(arg, Enum):
            return arg.value
        return json.JSONEncoder.default(self, arg)


def write_machine_code(filename: str, code: dict[str, str]) -> None:
    with open(filename, "w", encoding="utf-16") as f:
        json.dump(code, f, cls=CustomEncoder, indent=2)


def read_machine_code(filename: str) -> dict[str, str]:
    with open(filename, "r", encoding="utf-16") as f:
        return json.load(f)
