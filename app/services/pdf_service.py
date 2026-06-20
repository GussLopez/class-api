import fitz

def extract_pdf_pages(pdf_path: str):

    pdf = fitz.open(pdf_path)

    pages = []

    for page_num in range(len(pdf)):

        page = pdf[page_num]

        pages.append({
            "page": page_num + 1,
            "text": page.get_text()
        })

    return pages