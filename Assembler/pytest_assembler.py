import pytest
from assembler import Assembler


@pytest.fixture
def setup_files(tmp_path):
    asm_file = tmp_path / "test.asm"
    bin_file = tmp_path / "test.bin"
    log_file = tmp_path / "test_log.csv"
    return asm_file, bin_file, log_file


def test_load(setup_files):
    asm_file, bin_file, log_file = setup_files
    asm_file.write_text("LOAD 12 70\n")
    assembler = Assembler(str(asm_file), str(bin_file), str(log_file))
    assembler.assemble()
    with open(bin_file, "rb") as f:
        assert f.read() == bytes([0xCC, 0x08])


def test_read(setup_files):
    asm_file, bin_file, log_file = setup_files
    asm_file.write_text("READ 8 63\n")
    assembler = Assembler(str(asm_file), str(bin_file), str(log_file))
    assembler.assemble()
    with open(bin_file, "rb") as f:
        assert f.read() == bytes([0xE8, 0x07, 0x00, 0x00, 0x00])


def test_write(setup_files):
    asm_file, bin_file, log_file = setup_files
    asm_file.write_text("WRITE 24 451\n")
    assembler = Assembler(str(asm_file), str(bin_file), str(log_file))
    assembler.assemble()
    with open(bin_file, "rb") as f:
        assert f.read() == bytes([0x78, 0x38, 0x00, 0x00, 0x00])


def test_bswap(setup_files):
    asm_file, bin_file, log_file = setup_files
    asm_file.write_text("BSWAP 16 195 606\n")
    assembler = Assembler(str(asm_file), str(bin_file), str(log_file))
    assembler.assemble()
    with open(bin_file, "rb") as f:
        assert f.read() == bytes([0x70, 0x18, 0x00, 0x00, 0xC0, 0x4B, 0x00])