import fitz # PyMuPDF

def delete_word_by_index(input_pdf: str, output_pdf: str, page_number: int, word_index: int):
    """
    Deletes a specific word from a PDF page by redacting it.

    Args:
        input_pdf (str): Path to the original PDF file.
        output_pdf (str): Path to save the modified PDF file.
        page_number (int): The page number to modify (0-based).
        word_index (int): The index of the word to delete on that page.
    """
    try:
        # Open the PDF
        doc = fitz.open(input_pdf)
    except Exception as e:
        print(f"Error opening file: {e}")
        return

    # Check if the page number is valid
    if page_number >= len(doc):
        print(f"Error: Invalid page number. The document has only {len(doc)} pages.")
        doc.close()
        return

    # Select the page
    page = doc.load_page(page_number)

    # Get all words on the page
    words = page.get_text("words")

    # Check if the word index is valid
    if word_index >= len(words):
        print(f"Error: Invalid word index. Page {page_number + 1} has only {len(words)} words.")
        doc.close()
        return

    # Get the coordinates of the word to delete
    word_to_delete = words[word_index]
    x0, y0, x1, y1, _ = word_to_delete[:5]
    word_rect = fitz.Rect(x0, y0, x1, y1)

    # Add a redaction annotation for that word's area
    # By default, it will be filled with a black box
    page.add_redact_annot(word_rect)

    # Apply the redaction to permanently remove the word
    # This is the most important step!
    page.apply_redactions()

    # Save the changes to a new file
    doc.save(output_pdf)
    doc.close()
    
    print(f"Successfully deleted word at index {word_index} on page {page_number + 1}.")
    print(f"Modified PDF saved as: {output_pdf}")


if __name__ == "__main__":
    # --- Configuration ---
    file_to_edit = "ECG-Sample-Report.pdf"
    page_to_edit = 0  # Page 1 (0-based index)
    index_of_word_to_delete = 9 # The 11th word on the page
    output_file = "ECG-Report-redacted.pdf"
    
    delete_word_by_index(file_to_edit, output_file, page_to_edit, index_of_word_to_delete)