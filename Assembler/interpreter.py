import argparse
import csv

class Interpreter:
    def __init__(self, path_to_binary_file, path_to_result_file, boundaries):
        self.path_result = path_to_result_file
        self.boundaries = list(map(int, boundaries.split(':')))
        self.registers = [0] * (self.boundaries[1] - self.boundaries[0] + 1)
        self.stack = []
        with open(path_to_binary_file, 'rb') as binary_file:
            self.byte_code = int.from_bytes(binary_file.read(), byteorder="little")

    def interpret(self):
        while self.byte_code != 0:
            A = self.byte_code & ((1 << 5) - 1)
            self.byte_code >>= 5
            match A:
                case 12: self.load()
                case 8: self.read()
                case 24: self.write()
                case 16: self.bswap()
                case _: raise ValueError("В бинарном файле содержатся невалидные данные: неверный байт-код")
        with open(self.path_result, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Address", "Value"])
            for pos, register in enumerate(self.registers, self.boundaries[0]):
                csv_writer.writerow([pos, register])

    def load(self):
        B = self.byte_code & ((1 << 11) - 1); self.byte_code >>= 11
        self.stack.append(B)

    def read(self):
        B = self.byte_code & ((1 << 32) - 1); self.byte_code >>= 35
        if not (self.boundaries[0] <= B <= self.boundaries[1]):
            raise ValueError("В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")
        self.stack.append(self.registers[B])

    def write(self):
        B = self.byte_code & ((1 << 32) - 1); self.byte_code >>= 35
        if not (self.boundaries[0] <= B <= self.boundaries[1]):
            raise ValueError("В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")
        self.registers[B] = self.stack.pop()

    def bswap(self):
        B = self.byte_code & ((1 << 32) - 1); self.byte_code >>= 32
        C = self.byte_code & ((1 << 13) - 1); self.byte_code >>= 19
        if not (self.boundaries[0] <= B <= self.boundaries[1]):
            raise ValueError("В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")
        if not (self.boundaries[0] <= self.stack[-1] + C <= self.boundaries[1]):
            raise ValueError("В бинарном файле присутствуют невалидные данные: обращение к ячейки памяти по адресу вне диапазона")
        value = self.registers[B]
        value = value.to_bytes(2, byteorder="little")
        value1, value2 = value[0:1], value[1:2]
        value = value2 + value1
        value = int.from_bytes(value, byteorder="little")
        value = value & 0x7FF
        self.registers[self.stack.pop() + C] = value


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("bin_file", help="Входной файл (*.bin)")
    parser.add_argument("res_file", help="Выходной файл (*.csv)")
    parser.add_argument("boundaries", help="Границы памяти в формате: <левая>:<правая>")
    args = parser.parse_args()
    interpreter = Interpreter(args.bin_file, args.res_file, args.boundaries)
    try:
        interpreter.interpret()
        print(f"Интерпретация выполнена успешно. Результаты сохранены в {args.res_file}")
    except ValueError as error:
        print(f"Ошибка:\n{error}")
