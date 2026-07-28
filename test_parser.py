from pathlib import Path

from src.infrastructure.fb2_parser import FB2Parser


def print_chapters(chapters, level=0):
    for chapter in chapters:
        indent = "    " * level

        print(
            f"{indent}Глава: {chapter.title}"
        )

        for element in chapter.elements:
            print(
                f"{indent}  {type(element).__name__}: "
                f"{getattr(element, 'text', '')[:80]}"
            )

        print_chapters(
            chapter.children,
            level + 1,
        )


def main():
    parser = FB2Parser()

    book = parser.parse(
        Path(r"C:\Users\dmitr\OneDrive\Desktop\Трудно быть богом.fb2")
    )

    print(f"Название : {book.title}")
    print(f"Автор    : {book.author.full_name}")
    print(f"Язык     : {book.language}")

    print()
    print("Структура книги:")
    print_chapters(book.chapters)


if __name__ == "__main__":
    main()