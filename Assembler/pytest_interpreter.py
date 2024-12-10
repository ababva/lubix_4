import pytest
from interpreter import Interpreter


@pytest.fixture
def setup_binary_file(tmp_path):
    binary_file = tmp_path / "test.bin"
    result_file = tmp_path / "test_result.csv"
    return binary_file, result_file


def test_load(setup_binary_file):
    binary_file, result_file = setup_binary_file
    binary_file.write_bytes(bytes([0xCC, 0x08]))
    interpreter = Interpreter(str(binary_file), str(result_file), "0:1")
    interpreter.interpret()
    assert interpreter.stack[-1] == 70


def test_read(setup_binary_file):
    binary_file, result_file = setup_binary_file
    binary_file.write_bytes(bytes([0xE8, 0x07, 0x00, 0x00, 0x00]))
    interpreter = Interpreter(str(binary_file), str(result_file), "0:70")
    interpreter.registers[63] = 1
    interpreter.interpret()
    assert interpreter.stack[-1] == 1


def test_write(setup_binary_file):
    binary_file, result_file = setup_binary_file
    binary_file.write_bytes(bytes([0x78, 0x38, 0x00, 0x00, 0x00]))
    interpreter = Interpreter(str(binary_file), str(result_file), "0:500")
    interpreter.stack.append(1)
    interpreter.interpret()
    with open(result_file, "r", encoding="utf-8") as f:
        assert "451,1" in f.read()


def test_bswap(setup_binary_file):
    binary_file, result_file = setup_binary_file
    binary_file.write_bytes(bytes([0x70, 0x18, 0x00, 0x00, 0xC0, 0x4B, 0x00]))
    interpreter = Interpreter(str(binary_file), str(result_file), "0:650")
    interpreter.registers[195] = 10
    interpreter.stack.append(10)
    interpreter.interpret()
    with open(result_file, "r", encoding="utf-8") as f:
        assert "616,512" in f.read()