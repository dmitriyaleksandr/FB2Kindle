from pathlib import Path
import xml.etree.ElementTree as ET

from src.domain.book import Book


class FB2Parser:
    """Parses FB2 files into domain models."""

    FB2_NS = {"fb": "http://www.gribuser.ru/xml/fictionbook/2.0"}

    def parse(self, file_path: Path) -> Book:
        """Parse an FB2 file into a Book object."""

        tree = ET.parse(file_path)
        root = tree.getroot()

        return Book(
            title=self._parse_title(root),
            author=self._parse_author(root),
            language=self._parse_language(root),
        )

    def _parse_title(self, root: ET.Element) -> str:
        element = root.find(
            "fb:description/fb:title-info/fb:book-title",
            self.FB2_NS,
        )

        return element.text.strip() if element is not None and element.text else ""

    def _parse_author(self, root: ET.Element) -> str:
        first_name = root.find(
            "fb:description/fb:title-info/fb:author/fb:first-name",
            self.FB2_NS,
        )

        last_name = root.find(
            "fb:description/fb:title-info/fb:author/fb:last-name",
            self.FB2_NS,
        )

        parts = []

        if first_name is not None and first_name.text:
            parts.append(first_name.text.strip())

        if last_name is not None and last_name.text:
            parts.append(last_name.text.strip())

        return " ".join(parts)

    def _parse_language(self, root: ET.Element) -> str:
        element = root.find(
            "fb:description/fb:title-info/fb:lang",
            self.FB2_NS,
        )

        return element.text.strip() if element is not None and element.text else ""