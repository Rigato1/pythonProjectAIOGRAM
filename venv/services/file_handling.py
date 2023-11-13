import os
import sys


PAGE_SIZE = 1050

book: dict[int, str] = {}


# Функция, возвращающая строку с текстом страницы и ее размер
import re


def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    end = min(start + size, len(text))
    for i in range(end, start, -1):
        if i < len(text):
            if text[i - 1] in ".,!?;:" and text[i] not in ".,!?;:":
                end=i
                break
            else:
                i -= 2

        elif i >= len(text):
            if text[i - 1] in ".,;:!?":
                if text[i - 2] in ".,?!;:":
                    i -= 2
                else:
                    end=i
                    break

    page = text[start:i].rstrip()
    return page, len(page)

# Не удаляйте эти объекты - просто используйте
book: dict[int, str] = {}
PAGE_SIZE = 1050
BOOK_PATH='C:/Users/Мутагир/PycharmProjects/pythonProjectAIOGRAM/venv/book/book.txt'



def prepare_book(path: str) -> None:
    with open(path, 'r+', encoding="utf-8") as f:
        file = f.read()
    a = 0
    b = 1
    z = len(file)
    while a < z:
        r = _get_part_text(file, a, PAGE_SIZE)
        if r is not None:
            a += r[1]

        s = r[0].lstrip()
        dict1 = {b: s}
        b += 1
        book.update(dict1)
        dict1.clear




# Вызов функции prepare_book для подготовки книги из текстового файла
prepare_book(os.path.join(sys.path[0], os.path.normpath(BOOK_PATH)))