import fitz
import pytesseract
from PIL import Image
import io

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


class PDFReaderTool:

    def read_pdf(self, pdf_path):

        doc = fitz.open(pdf_path)

        pages = []

        for page_num in range(len(doc)):

            page = doc[page_num]

            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

            img = Image.open(
                io.BytesIO(
                    pix.tobytes("png")
                )
            )

            text = pytesseract.image_to_string(img)

            print(
                f"Page {page_num+1}: "
                f"{len(text)} chars extracted"
            )

            pages.append({
                "document": pdf_path,
                "page": page_num + 1,
                "text": text
            })

        return pages