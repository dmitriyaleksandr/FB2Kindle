from pathlib import Path

from src.domain.book import Book


class FB2Parser:
    """Parses FB2 files into domain models."""

    def parse(self, file_path: Path) -> Book:
        """
        Parse an FB2 file.

        Args:
            file_path: Path to the FB2 file.

        Returns:
            Book: Parsed book model.
        """
        raise NotImplementedError("FB2 parser is not implemented yet.")