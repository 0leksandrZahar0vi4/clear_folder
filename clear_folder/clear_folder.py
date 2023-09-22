import os
from pathlib import Path
import sys
import shutil


CATEGORIES = {
    "AUDIO": [".mp3", ".wav", ".flac", ".wma"],
    "DOCS": [".docx", ".txt", ".pdf", ".xlsx", "xls", ".pptx", ".doc"],
    "PICT": [".jpeg", ".png", ".jpg", ".svg"],
    "MOVIES": [".avi", ".mp4", ".mov", ".mkv"],
    "ARHiVE": [".zip", ".gz", ".tar"],
}


CYRILLIC_SYMBOLS = "aбвгдeёжзийклмнопpcтyфхцчшщъыьэюяєiїґ"
TRANSLATION = (
    "a",
    "b",
    "v",
    "g",
    "d",
    "e",
    "e",
    "j",
    "z",
    "u",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "r",
    "s",
    "t",
    "u",
    "f",
    "h",
    "ts",
    "ch",
    "sh",
    "sch",
    "",
    "u",
    "",
    "e",
    "yu",
    "ya",
    "je",
    "i",
    "ji",
    "g",
)
TRANS = {}
SYMB = ("!", "№", "$", "%", "&", "(", ")", "+", "-", "_", "#", " ")

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()
    TRANS[ord(c.lower())] = l.lower()

for i in SYMB:
    TRANS[ord(i)] = "_"


def normalize(file: Path) -> None:
    return file.translate(TRANS)


f = []


def get_categories(file: Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "OTHER"


def move_file(file: Path, category: str, root_dir: Path) -> None:
    target_dir = root_dir.joinpath(category)
    if not target_dir.exists():
        target_dir.mkdir()
    new_path = target_dir.joinpath(normalize(file.stem) + file.suffix)
    if not new_path.exists():
        file.replace(new_path)
    if file.is_file() and file.suffix in [
        ".zip",
        ".gz",
        ".tar",
    ]:
        shutil.unpack_archive(file, target_dir)


def sort_folder(path: Path) -> None:
    for element in path.glob("**/*"):
        if element.is_file():
            category = get_categories(element)
            move_file(element, category, path)
        # if element.suffix in [".zip", ".gz", ".tar"]:
        #     shutil.unpack_archive(element, category)
        if element.is_dir():
            if element.stat().st_size == 0:
                try:
                    os.rmdir(element)
                except OSError:
                    continue


# def unpack_file(file: Path, category: str, root_dir: Path):
#     target_dir = root_dir.joinpath(category)
#     if file.is_file() and file.suffix in [
#         ".zip",
#         ".gz",
#         ".tar",
#     ]:
#         shutil.unpack_archive(file, category)
#     return shutil.unpack_file(file, category)


def append_list(path: Path, category):
    for element in path.glob("**/*"):
        if element.is_file():
            print(element.name, category)
        return element.name, category


# def del_folder(path: Path) -> None:
#     for element in path.glob("**/*"):
#         print(element)
#         if element.is_dir():
#             while element.stat().st_size == 0:
#                 if element.stat().st_size == 0:
#                     try:
#                         os.rmdir(element)
#                     except OSError:
#                         continue
#             return del_folder(element)


def main():
    try:
        path = Path(sys.argv[1])

    except IndexError:
        return "No path to folder"

    if not path.exists():
        return "Folder does not exists"

    sort_folder(path)
    return "All ok"


if __name__ == "__main__":
    main()
