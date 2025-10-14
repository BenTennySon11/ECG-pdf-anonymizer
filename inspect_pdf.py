import fitz

def inspect_pdf(pdf_path: str):
    doc = fitz.open(pdf_path)
    print(f"PDF has {len(doc)} pages.")

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        print(f"\nPage {page_num + 1}:")
        images = page.get_images(full=True)
        print(f"  Raster images: {len(images)}")
        if images:
            for img in images:
                print(f"    Image xref: {img[0]}, size: {img[2]}x{img[3]}")

        # Check for drawings (vector graphics)
        drawings = page.get_drawings()
        print(f"  Vector drawings: {len(drawings)}")

        # Get text blocks
        text = page.get_text()
        print(f"  Text length: {len(text)} characters")

    doc.close()

if __name__ == "__main__":
    inspect_pdf("ECG-Sample-Report.pdf")
