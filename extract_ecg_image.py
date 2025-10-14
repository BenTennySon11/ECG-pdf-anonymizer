import fitz

def extract_ecg_image(pdf_path: str, output_dir: str = "."):
    """
    Extracts the ECG image from the PDF by redacting text and rendering the page as an image.
    Assumes the ECG is on a page with many vector drawings (likely the graph).
    """
    doc = fitz.open(pdf_path)
    image_count = 0

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        drawings = page.get_drawings()
        if len(drawings) > 10000:  # Assuming ECG pages have many vector elements
            # Redact all text blocks
            text_dict = page.get_text("dict")
            for block in text_dict["blocks"]:
                if "lines" in block:  # Text block
                    for line in block["lines"]:
                        for span in line["spans"]:
                            bbox = span["bbox"]
                            page.add_redact_annot(bbox, fill=(1, 1, 1))  # White fill
            
            # Apply redactions
            page.apply_redactions()
            
            # Render the page to an image
            pix = page.get_pixmap(dpi=600)  # Higher DPI for better quality
            image_filename = f"ecg_image_{page_num}.png"
            pix.save(f"{output_dir}/{image_filename}")
            print(f"Saved: {image_filename}")
            image_count += 1

    doc.close()
    print(f"Total images extracted: {image_count}")

if __name__ == "__main__":
    extract_ecg_image("ECG-Sample-Report.pdf")
