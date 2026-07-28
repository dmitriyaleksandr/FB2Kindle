from pathlib import Path

from src.domain.elements import (
    DocumentElement,
)
from src.infrastructure.fb2_parser import FB2Parser


def count_elements(chapters):
    counts = {}

    def process_chapter(chapter):
        for element in chapter.elements:
            name = type(element).__name__
            counts[name] = counts.get(name, 0) + 1

        for child in chapter.children:
            process_chapter(child)

    for chapter in chapters:
        process_chapter(chapter)

    return counts


def print_structure(chapters, level=0, limit=5):
    printed = 0

    for chapter in chapters:

        if printed >= limit:
            print("    " * level + "...")
            break

        indent = "    " * level

        print(
            f"{indent}Глава: {chapter.title or '[без названия]'}"
        )

        for element in chapter.elements[:5]:
            print(
                f"{indent}  - {type(element).__name__}"
            )

        if len(chapter.elements) > 5:
            print(
                f"{indent}  ..."
            )

        print_structure(
            chapter.children,
            level + 1,
            limit,
        )

        printed += 1


def main():

    parser = FB2Parser()

    book = parser.parse(
        Path(r"C:\Users\dmitr\OneDrive\Desktop\Трудно быть богом.fb2")
    )

    print(f"Название: {book.title}")
    print(f"Автор: {book.author.full_name}")
    print(f"Язык: {book.language}")

    print()

    print(
        f"Глав верхнего уровня: "
        f"{len(book.chapters)}"
    )

    counts = count_elements(
        book.chapters
    )

    print()
    print("Элементы документа:")

    for name, count in counts.items():
        print(
            f"  {name}: {count}"
        )

    print()
    print("Структура книги:")

    print_structure(
        book.chapters
    )


if __name__ == "__main__":
    main()