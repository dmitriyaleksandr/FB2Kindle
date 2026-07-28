from pathlib import Path

from src.infrastructure.fb2_parser import FB2Parser


def main():
    parser = FB2Parser()

    book = parser.parse(Path(r"C:\Users\dmitr\OneDrive\Desktop\Трудно быть богом.fb2"))

    print(f"Название : {book.title}")
    print(f"Автор     : {book.author}")
    print(f"Язык      : {book.language}")


if __name__ == "__main__":
    main()