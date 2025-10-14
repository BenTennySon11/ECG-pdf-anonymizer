import fitz
def pdfreader(path:str):
    doc=fitz.open(path)
    print(f"Total Pages:{len(doc)}")
    for num in range(len(doc)):
        page=doc.load_page(num)
        print(f"\n {num+1}:")
        images = page.get_images(full=True)
        print(f"images: {len(images)}")
        if images:
            for img in images:
                print(f"image xref:{img[0]},size:{img[2]}x{img[3]}")
        drawings=page.get_drawings()
        print(f"vector drawings:{len(drawings)}")

        text=page.get_text()
        print(f"text length:{len(text)} characters")
    doc.close()
if __name__ == "__main__":
    pdfreader("ECG-Sample-Report.pdf")
