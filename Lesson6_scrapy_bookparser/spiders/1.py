"""
Class File make file-object, writing in it, supporting iteration line
by line, and concatenation 2 instances of class File in 1 new object,
located in temp folder
"""

import os
import tempfile


class File:
    def __init__(self, path):
        self.path = path
        with open(self.path, "w", encoding="utf-8") as self.f:
            print("Creating the file with specified path...")
            print(f"File-object {self.f.name} successfully created")

    def __iter__(self):
        self.f = open(self.path, "r", encoding="utf-8")
        return self.f

    def __next__(self):
        line = self.f.readline()
        if not line:
            self.f.close()
            raise StopIteration
        return line

    def write(self, some_write):
        with open(self.path, "w", encoding="utf-8") as self.f:
            self.f.write(some_write)

    def read(self):
        with open(self.path, "r", encoding="utf-8") as self.f:
            return self.f.read()

    def __add__(self, term):
        try:
            sum_path = os.path.join(tempfile.gettempdir(), "sum_file.txt")
            sum_file = File(sum_path)
            content = ''
            for i in [self, term]:
                content += i.read()
            sum_file.write(content)
            print("Result of summing in:", sum_path)
            return sum_file
        except IOError as err:
            print(err.args[0], err.args[1], err.args[2])

    def __str__(self):
        return self.path


def main(path):
    first = File(os.path.join(path, "file_1.txt"))
    first.write("Это первое слагаемое Это добавка второй строки для принт")
    second = File(os.path.join(path, "file_2.txt"))
    second.write("А это уже второе слагаемое Вау, оно такое неожиданное")
    for _ in first:
        print(_)
    third = first + second
    print(third.read())


if __name__ == "__main__":
    path = "u:\PyCharm Projects\Coursera_Python_MFTI_mailru"
    main(path)