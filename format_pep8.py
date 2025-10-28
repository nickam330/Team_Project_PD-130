import autopep8
import sys


def format_file(file_path: str, inplace: bool = True):
    """
    Форматирует Python-файл по стандарту PEP8.

    :param file_path: путь к файлу с кодом
    :param inplace: если True, перезаписывает файл, иначе возвращает форматированный текст
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    formatted_code = autopep8.fix_code(code, options={'aggressive': 1})

    if inplace:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(formatted_code)
        print(f"Файл {file_path} отформатирован по PEP8.")
    else:
        return formatted_code


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python format_pep8.py <путь_к_файлу>")
        sys.exit(1)

    file_path = sys.argv[1]
    format_file(file_path)