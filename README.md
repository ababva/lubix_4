# Задание №4
Разработать ассемблер и интерпретатор для учебной виртуальной машины
(УВМ). Система команд УВМ представлена далее.
Для ассемблера необходимо разработать читаемое представление команд
УВМ. Ассемблер принимает на вход файл с текстом исходной программы, путь к
которой задается из командной строки. Результатом работы ассемблера является
бинарный файл в виде последовательности байт, путь к которому задается из
командной строки. Дополнительный ключ командной строки задает путь к файлулогу, в котором хранятся ассемблированные инструкции в духе списков
“ключ=значение”, как в приведенных далее тестах.
Интерпретатор принимает на вход бинарный файл, выполняет команды УВМ
и сохраняет в файле-результате значения из диапазона памяти УВМ. Диапазон
также указывается из командной строки.
Форматом для файла-лога и файла-результата является csv.
Необходимо реализовать приведенные тесты для всех команд, а также
написать и отладить тестовую программу.
Загрузка константы
| A | B | 
| - | - |
| Биты 0—4 | Биты 5—15 |
| 12 | Константа |

Размер команды: 2 байт. Операнд: поле B. Результат: новый элемент на стеке.
Тест (A=12, B=70):
0xCC, 0x08

**Чтение значения из памяти**

| A | B | 
| - | - | 
| Биты 0—4 | Биты 5-36 |
| 8 | Адрес |

Размер команды: 5 байт. Операнд: значение в памяти по адресу, которым
является поле B. Результат: новый элемент на стеке.
Тест (A=8, B=63):
0xE8, 0x07, 0x00, 0x00, 0x00

**Запись значения в память**

| A | B |
| - | - |
| Биты 0—4 | Биты 5-36 |
| 24 | Адрес | 

Размер команды: 5 байт. Операнд: элемент, снятый с вершины стека.
Результат: значение в памяти по адресу, которым является поле B.
Тест (A=24, B=451):
0x78, 0x38, 0x00, 0x00, 0x00

**Унарная операция: bswap()**

| A | B | C |
| - | - | - | 
| Биты 0—4 | Биты 5—36 |  Биты 37-49 | 
| 16 | Адрес | Смещение |

Размер команды: 7 байт. Операнд: значение в памяти по адресу, которым
является поле B. Результат: значение в памяти по адресу, которым является сумма
адреса (элемент, снятый с вершины стека) и смещения (поле C).
Тест (A=16, B=195, C=606):
0x70, 0x18, 0x00, 0x00, 0xC0, 0x4B, 0x00

Тестовая программа
Выполнить поэлементно операцию bswap() над вектором длины 4. Результат
записать в исходный вектор.

# Установка

## Клонирование репозитория
```git clone https://github.com/ababva/lubix_4```

## Скачивание библиотеки pytest:
```script.sh```
# Запуск
## Запуск assembler.py
```py .\assembler.py <path/to/program.csv> <path/to/bin_file.bin> -l <path/to/log.csv>```
## Запуск interpreter.py:
```py interpreter.py <path/to/bin_file.bin> <path/to/result.csv> <left_boundary:right_boundary>```
## Запуск pytest_assembler.py:
```pytest -v pytest_assembler.py```
## Запуск pytest_interpreter.py:
```pytest -v pytest_interpreter.py```
# Тесты
## Тестовая программа: 
### Выполнить поэлементно операцию pow() над двумя векторами длины 6.
Результат записать во второй вектор 
Входные данные:
A = (1, 2, 3, 4)
``` LOAD 12 1
LOAD 12 2
LOAD 12 3
LOAD 12 4

WRITE 24 8
WRITE 24 9
WRITE 24 10
WRITE 24 11

LOAD 12 1
LOAD 12 2
LOAD 12 3
LOAD 12 4

BSWAP 16 8 4
BSWAP 16 9 6
BSWAP 16 10 8
BSWAP 16 11 10
````
Выходные данные:
(256, 512, 768, 1024)
``` 2,0
3,0
4,0
5,0
6,0
7,0
8,1024
9,768
10,512
11,256
12,0
13,0
14,0
15,0
16,0
17,0
18,0
19,0
20,0
21,0
22,0
23,0
24,0
25,0
```
# Ассемблер
## Проверка, что инструкция LOAD корректно обрабатывается и генерирует правильный двоичный код
```def test_load(setup_files):
    asm_file, bin_file, log_file = setup_files
    asm_file.write_text("LOAD 12 70\n")
    assembler = Assembler(str(asm_file), str(bin_file), str(log_file))
    assembler.assemble()
    with open(bin_file, "rb") as f:
        assert f.read() == bytes([0xCC, 0x08])
```
## Проверка, что инструкция READ корректно обрабатывается и генерирует правильный двоичный код.
``` def test_read(setup_files):
    asm_file, bin_file, log_file = setup_files
    asm_file.write_text("READ 8 63\n")
    assembler = Assembler(str(asm_file), str(bin_file), str(log_file))
    assembler.assemble()
    with open(bin_file, "rb") as f:
        assert f.read() == bytes([0xE8, 0x07, 0x00, 0x00, 0x00])
```
## Проверка, что инструкция WRITE корректно обрабатывается и генерирует правильный двоичный код.
```def test_write(setup_files):
    asm_file, bin_file, log_file = setup_files
    asm_file.write_text("WRITE 24 451\n")
    assembler = Assembler(str(asm_file), str(bin_file), str(log_file))
    assembler.assemble()
    with open(bin_file, "rb") as f:
        assert f.read() == bytes([0x78, 0x38, 0x00, 0x00, 0x00])
```
## Проверка, что инструкция BSWAP корректно обрабатывается и генерирует правильный двоичный код.
```def test_bswap(setup_files):
    asm_file, bin_file, log_file = setup_files
    asm_file.write_text("BSWAP 16 195 606\n")
    assembler = Assembler(str(asm_file), str(bin_file), str(log_file))
    assembler.assemble()
    with open(bin_file, "rb") as f:
        assert f.read() == bytes([0x70, 0x18, 0x00, 0x00, 0xC0, 0x4B, 0x00])
```
## Результаты
![image](https://github.com/user-attachments/assets/9c7623ce-aef7-4be7-af6b-ac85ca554f38)

# Интерпретатор
## Тест загрузка константы
```def test_load(setup_binary_file):
    binary_file, result_file = setup_binary_file
    binary_file.write_bytes(bytes([0xCC, 0x08]))
    interpreter = Interpreter(str(binary_file), str(result_file), "0:1")
    interpreter.interpret()
    assert interpreter.stack[-1] == 70
```
## Тест Чтение
```
def test_read(setup_binary_file):
    binary_file, result_file = setup_binary_file
    binary_file.write_bytes(bytes([0xE8, 0x07, 0x00, 0x00, 0x00]))
    interpreter = Interpreter(str(binary_file), str(result_file), "0:70")
    interpreter.registers[63] = 1
    interpreter.interpret()
    assert interpreter.stack[-1] == 1
```
## Тест Запись
```
def test_write(setup_binary_file):
    binary_file, result_file = setup_binary_file
    binary_file.write_bytes(bytes([0x78, 0x38, 0x00, 0x00, 0x00]))
    interpreter = Interpreter(str(binary_file), str(result_file), "0:500")
    interpreter.stack.append(1)
    interpreter.interpret()
    with open(result_file, "r", encoding="utf-8") as f:
        assert "451,1" in f.read()
```
## Тест bswap()
```
def test_bswap(setup_binary_file):
    binary_file, result_file = setup_binary_file
    binary_file.write_bytes(bytes([0x70, 0x18, 0x00, 0x00, 0xC0, 0x4B, 0x00]))
    interpreter = Interpreter(str(binary_file), str(result_file), "0:650")
    interpreter.registers[195] = 10
    interpreter.stack.append(10)
    interpreter.interpret()
    with open(result_file, "r", encoding="utf-8") as f:
        assert "616,512" in f.read()
```
# Результаты
![image](https://github.com/user-attachments/assets/92f175a4-1f84-45c6-808b-a15f0a7c11d7)

