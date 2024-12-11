import re

from pypdf import PdfReader

from .logger import log

class Extractor:
    def __init__(self) -> None:
        op: str = "utils.extractor.Extractor.__init__"

        log.debug(f"Initializing extractor class [{op}]")

    def extract_pdf(self, path: str, max_pages: int = 5) -> str:
        op: str = "utils.extractor.Extractor.extract_pdf"

        try:
            log.debug(f"Initializing a PdfReader object {path}")
            reader = PdfReader(path)

            log.debug("Extracting metadata")
            meta = reader.metadata

            total_pages = len(reader.pages)
            selected_pages = range(min(total_pages, max_pages))
            log.debug(f"Selecting first {len(selected_pages)} pages to extract text")

            text = " ".join(reader.pages[page].extract_text() for page in selected_pages)

            clean_text = " ".join(text.split())

            return f"Title: {meta.title} Text: {clean_text}"

        except Exception as e:
            log.error(f"Error extracting the text of PDF file [{op}] \n{e}")
            raise

    def extract_keywords(self, summary: str) -> list[str] | None:
        op: str = "utils.extractor.Extractor.extract_keywords"

        try:
            match = re.search(r"keywords:\s*\[(.*?)\]", summary)

            if match:
                keywords_str = match.group(1)
                keywords = [keyword.strip() for keyword in keywords_str.split(",")]

            return keywords

        except Exception as e:
            log.error(f"Error extracting the keywords from summary [{op}] \n{e}")
            raise


extractor = Extractor()
