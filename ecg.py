import fitz  # PyMuPDF library for editing PDFs
import os

def redact_name(input_pdf: str, output_pdf: str, name_to_remove: str):
    """
    Finds and redacts a user-specified name from all pages of a PDF.

    Args:
        input_pdf (str): Path to the original PDF.
        output_pdf (str): Path to save the anonymized PDF.
        name_to_remove (str): The patient name to redact.
    """
    if not name_to_remove:
        print("❌ No name provided. Aborting process.")
        return

    if not os.path.exists(input_pdf):
        print(f"❌ ERROR: The file '{input_pdf}' was not found in the current directory.")
        return

    print(f"\nSearching for '{name_to_remove}' and redacting...")
    doc = None
    try:
        doc = fitz.open(input_pdf)
        total_redactions = 0
        
        # Loop through every page in the document
        for page_num, page in enumerate(doc): # type: ignore
            # Search for the name on the current page
            areas = page.search_for(name_to_remove)
            
            if areas:
                total_redactions += len(areas)
                for area in areas:
                    # Apply a white redaction box over each found instance
                    page.add_redact_annot(area, fill=(1, 1, 1))
                
                # Make the redactions permanent for this page
                page.apply_redactions()
                print(f"--- Page {page_num + 1}: Found and removed {len(areas)} instance(s).")
            else:
                print(f"--- Page {page_num + 1}: Name not found.")
        
        # Save the modified document to a new file
        doc.save(output_pdf, garbage=4, deflate=True, clean=True)
        
        print("\n-------------------------------------------")
        if total_redactions > 0:
            print(f"🎉 Success! Process complete.")
            print(f"Total redactions performed: {total_redactions}")
            print(f"Anonymized file saved as: '{output_pdf}'")
        else:
            print(f"⚠️ Warning: The name '{name_to_remove}' was not found anywhere in the document.")

    except Exception as e:
        print(f"An unexpected error occurred during redaction: {e}")
    finally:
        if doc and not doc.is_closed:
            doc.close()

# --- Main execution block ---
if __name__ == "__main__":
    input_file = "ECG-Sample-Report.pdf"
    output_file = "Anonymized-ECG-Report.pdf"
    
    # --- Interactive Step ---
    # Ask the user for the name that needs to be removed.
    patient_name = input("Please enter the full patient name to remove (e.g., Willy McKee): ")
    
    # Run the redaction process with the provided name
    redact_name(input_file, output_file, patient_name)