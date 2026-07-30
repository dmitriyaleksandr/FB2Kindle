from pathlib import Path

from src.exporters.epub_builder import EPUBBuilder
from src.infrastructure.fb2_parser import FB2Parser


def main():

    parser = FB2Parser()

    book = parser.parse(
        Path(
            r"C:\Users\dmitr\OneDrive\Desktop\Трудно быть богом.fb2"
        )
    )

    print("=" * 60)
    print(f"Book title: {book.title}")
    print(f"Top-level chapters: {len(book.chapters)}")
    print()

    if book.chapters:

        first = book.chapters[0]

        print("FIRST CHAPTER")
        print(f"Title    : {first.title!r}")
        print(f"Elements : {len(first.elements)}")
        print(f"Children : {len(first.children)}")
        print()

        print("ELEMENT TYPES:")

        for i, element in enumerate(first.elements, start=1):
            print(f"{i}. {type(element).__name__}")

    builder = EPUBBuilder()

    builder.build(
        book,
        "output.epub",
    )

    print()
    print("EPUB successfully created.")


if __name__ == "__main__":
    main()