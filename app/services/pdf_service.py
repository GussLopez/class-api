import fitz

def extract_pages(path: str):
  pdf = fitz.open(path)

  pages = []

  for page_number in range(len(pdf)):

      page = pdf[page_number]

      pages.append({
          "page": page_number + 1,
          "text": page.get_text()
      })

  return pages