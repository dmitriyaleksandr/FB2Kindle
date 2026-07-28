import base64
import xml.etree.ElementTree as ET


class ResourceExtractor:
    """Extracts binary resources from FB2 files."""

    FB2_NS = {
        "fb": "http://www.gribuser.ru/xml/fictionbook/2.0"
    }

    def extract(
        self,
        root: ET.Element,
    ) -> dict[str, bytes]:
        """
        Extract binary resources from FB2 XML.

        Returns:
            Dictionary with resource id as key
            and decoded bytes as value.
        """

        resources = {}

        for binary in root.findall(
            "fb:binary",
            self.FB2_NS,
        ):
            resource_id = binary.attrib.get(
                "id"
            )

            if not resource_id:
                continue

            if binary.text is None:
                continue

            try:
                resources[resource_id] = (
                    base64.b64decode(
                        binary.text.strip()
                    )
                )

            except Exception:
                continue

        return resources