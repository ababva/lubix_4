import argparse
import csv

class Assembler:
    def __init__(self, path_to_code_file, path_to_binary_file, path_to_log_file):
        self.path_binary = path_to_binary_file
        self.path_code = path_to_code_file
        self.path_log = path_to_log_file
        self.bytes = []
        self.log_data = []

    def assemble(self):
        with open(self.path_code, 'rt') as code:
            for line in code:
                line = line.split('\n')[0].strip()
                if not line: continue
                command, *args = line.split()
                match command:
                    case "LOAD":
                        if len(args) != 2:
                            raise SyntaxError(f"{line}\nУ операции \"Загрузка константы\" должно быть 2 аргумента")
                        self.bytes.append(self.load(int(args[0]), int(args[1])))
                    case "READ":
                        if len(args) != 2:
                            raise SyntaxError(f"{line}\nУ операции \"Чтение значения из памяти\" должно быть 2 аргумента")
                        self.bytes.append(self.read(int(args[0]), int(args[1])))
                    case "WRITE":
                        if len(args) != 2:
                            raise SyntaxError(f"{line}\nУ операции \"Запись значения в память\" должно быть 2 аргумента")
                        self.bytes.append(self.write(int(args[0]), int(args[1])))
                    case "BSWAP":
                        if len(args) != 3:
                            raise SyntaxError(f"{line}\nУ операции \"Унарная операция: bswap()\" должно быть 3 аргумента")
                        self.bytes.append(self.bswap(int(args[0]), int(args[1]), int(args[2])))
                    case _:
                        raise SyntaxError(f"{line}\nНеизвестная операция")
        with open(self.path_binary, 'wb') as binary:
            for byte in self.bytes:
                binary.write(byte)
        if self.path_log:
            with open(self.path_log, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["Operation", "A", "B", "C", "Bytes"])
                csv_writer.writerows(self.log_data)

    def load(self, A, B):
        if A != 12: raise ValueError("Параметр А должен быть равен 12")
        if not (0 <= B < (1 << 11)): raise ValueError("Адрес B должен быть в пределах от 0 до 2047 (2^11-1)")
        bits = (B << 5) | A
        bits = bits.to_bytes(2, byteorder="little")
        self.log_data.append(["LOAD", A, B, None, bits.hex()])
        return bits

    def read(self, A, B):
        if A != 8: raise ValueError("Параметр А должен быть равен 8")
        if not (0 <= B < (1 << 32)): raise ValueError("Адрес B должен быть в пределах от 0 до 4294967295 (2^32-1)")
        bits = (B << 5) | A
        bits = bits.to_bytes(5, byteorder="little")
        self.log_data.append(["READ", A, B, None, bits.hex()])
        return bits

    def write(self, A, B):
        if A != 24: raise ValueError("Параметр А должен быть равен 24")
        if not (0 <= B < (1 << 32)): raise ValueError("Адрес B должен быть в пределах от 0 до 4294967295 (2^32-1)")
        bits = (B << 5) | A
        bits = bits.to_bytes(5, byteorder="little")
        self.log_data.append(["WRITE", A, B, None, bits.hex()])
        return bits

    def bswap(self, A, B, C):
        if A != 16: raise ValueError("Параметр А должен быть равен 16")
        if not (0 <= B < (1 << 32)): raise ValueError("Адрес B должен быть в пределах от 0 до 4294967295 (2^32-1)")
        if not (0 <= C < (1 << 13)): raise ValueError("Адрес C должен быть в пределах от 0 до 8191 (2^13-1)")
        bits = (C << 37) | (B << 5) | A
        bits = bits.to_bytes(7, byteorder="little")
        self.log_data.append(["BSWAP", A, B, C, bits.hex()])
        return bits


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("asm_file", help="Входной файл (*.asm)")
    parser.add_argument("bin_file", help="Выходной файл (*.bin)")
    parser.add_argument("-l", "--log_file", help="Лог файл (*.csv)")
    args = parser.parse_args()
    assembler = Assembler(args.asm_file, args.bin_file, args.log_file)
    try:
        assembler.assemble()
        print(f"Ассемблирование выполнено успешно. Выходной файл: {args.bin_file}")
    except ValueError as error:
        print(f"Ошибка:\n{error}")
