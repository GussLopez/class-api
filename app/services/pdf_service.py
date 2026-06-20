import fitz

def extract_pdf_pages(path: str):

  pdf = fitz.open(path)

  pages = []

  for page_index in range(len(pdf)):

      page = pdf[page_index]

      pages.append({
          "page": page_index + 1,
          "text": page.get_text()
      })

  return pages