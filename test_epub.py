from pathlib import Path

from src.exporters.epub_builder import EPUBBuilder
from src.infrastructure.fb2_parser import FB2Parser


def main():
    parser = FB2Parser()

    book = parser.parse(
        Path(r"C:\Users\dmitr\OneDrive\Desktop\Трудно быть богом.fb2")
    )

    builder = EPUBBuilder()

    output_file = Path("output.epub")

    builder.build(
        book,
        output_file,
    )

    print(f"EPUB создан: {output_file.resolve()}")


if __name__ == "__main__":
    main()