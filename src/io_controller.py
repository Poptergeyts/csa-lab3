from collections import deque


class IO:
    def __init__(self, input_buffer: list[int]):
        self.output = ""
        self.input_buffer = deque(input_buffer)

    def write_byte(self, value: int):
        if value == 0:
            self.output += "\n"
        else:
            char = chr(value)
            if char.isalnum() or char.isprintable():
                self.output += char
            else:
                self.output += str(value)

    def read_byte(self) -> int:
        if not self.input_buffer:
            raise EOFError("Input is over")
        return self.input_buffer.popleft()

    def __repr__(self) -> str:
        return f"{map(chr, self.input_buffer)}"
