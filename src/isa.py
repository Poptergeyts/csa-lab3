from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional


class Opcode(Enum):
    HLT = "hlt"
    JMP = "jmp"
    JZ = "jz"
    JNZ = "jnz"
    PUSH = "push"
    POP = "pop"
    SWAP = "swap"
    LD = "ld"
    ST = "st"
    INC = "inc"
    ADD = "add"
    SUB = "sub"
    MUL = "mul"
    DIV = "div"
    XOR = "xor"
    TEST = "test"


@dataclass
class Command:
    code: Opcode
    arg: Optional[int | str] = None

    def to_dict(self) -> dict:
        data = asdict(self)
        return {key: val for key, val in data.items()}

    @staticmethod
    def from_dict(data: dict):
        return Command(data["code"], data["arg"] if "arg" in data else None)

    def __str__(self) -> str:
        return str(self.to_dict())
