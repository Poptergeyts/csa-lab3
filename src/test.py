import contextlib
import io
import logging
import os
import tempfile

import pytest

import machine
import translator


@pytest.mark.golden_test("tests/*.yml")
def test_translator_and_machine(golden, caplog):
    caplog.set_level(logging.DEBUG)

    with tempfile.TemporaryDirectory() as tmpdirname:
        source = os.path.join(tmpdirname, "source.asm")
        input_file = os.path.join(tmpdirname, "input.txt")
        code = os.path.join(tmpdirname, "code.json")
        data = os.path.join(tmpdirname, "data.json")
        with open(source, "w", encoding="utf-8") as file:
            file.write(golden["asm"])
        with open(input_file, "w", encoding="utf-8") as file:
            file.write(golden["input"])
        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            translator.main(source, data, code)
            machine.main(code, data, input_file)

        with open(code, encoding="utf-16") as file:
            code = file.read()
        with open(data, encoding="utf-16") as file:
            data = file.read()
        assert code == golden.out["code_json"]
        assert data == golden.out["data_json"]
        assert stdout.getvalue() == golden.out["output"]
