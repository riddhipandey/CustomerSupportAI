from pypdf import PdfReader

class PDFService:
    def extract_pdf_text(self, file_path : str):
        reader = PdfReader(file_path)

        pages = []

        for page_number, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text()

            if page_text:
                page_info = {
                    "text" : page_text,
                    "page_number" : page_number
                }

                pages.append(page_info)

        return pages

    