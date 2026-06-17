
# DOCUMENT LOADER
# Reads PDF, DOCX, and TXT files
# and extracts their text content


import os
from pathlib import Path

# PyPDF2 - For reading PDF files
import PyPDF2

# python-docx - For reading Word documents
from docx import Document


def load_pdf(file_path):
    """
    Reads a PDF file and returns the extracted text.

    Real-life example:
    Just like a scanner reads a document,
    this function reads a PDF and extracts its text.
    """
    text = ""

    try:
        # Open the PDF file
        with open(file_path, 'rb') as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)

            # Get total number of pages
            total_pages = len(pdf_reader.pages)
            print(f"The PDF contains a total of {total_pages} pages")

            # Extract text from each page
            for page_num in range(total_pages):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()

                if page_text:
                    text += f"\n--- Page {page_num + 1} ---\n"
                    text += page_text

        print("PDF read successfully!")
        return text

    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None


def load_docx(file_path):
    """
    Reads a DOCX (Word) document and returns its text.
    """
    text = ""

    try:
        # Open the Word document
        doc = Document(file_path)

        # Extract text from each paragraph
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text += paragraph.text + "\n"

        print("Word document read successfully!")
        return text

    except Exception as e:
        print(f"Error reading DOCX file: {e}")
        return None


def load_txt(file_path):
    """
    Reads a plain text file and returns its content.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        print("Text file read successfully!")
        return text

    except Exception as e:
        print(f"Error reading TXT file: {e}")
        return None


def load_document(file_path):
    """
    MAIN FUNCTION - Automatically detects whether the file is
    a PDF, DOCX, or TXT file and calls the appropriate function
    to extract text.

    Real-life example:
    Just like a receptionist identifies the type of form
    and sends it to the correct department, this function
    identifies the file type and processes it accordingly.
    """

    # Get the file extension (.pdf, .docx, .txt)
    file_extension = Path(file_path).suffix.lower()

    print(f"\nLoading file: {file_path}")
    print(f"File type: {file_extension}")

    # Call the appropriate function based on the file extension
    if file_extension == '.pdf':
        return load_pdf(file_path)

    elif file_extension == '.docx':
        return load_docx(file_path)

    elif file_extension == '.txt':
        return load_txt(file_path)

    else:
        print(f"Sorry! This file type is not supported: {file_extension}")
        print("Supported types: PDF, DOCX, TXT")
        return None



# FOR TESTING
# This code runs only when the file
# is executed directly


if __name__ == "__main__":
    print("Running Document Loader Test...")
    print("=" * 40)

    # Create a test text file
    test_file = "test_document.txt"

    # Create sample content
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("This is a test document.\n")
        f.write("Created for the DocuMind project.\n")
        f.write("We will ask questions about this text using AI.\n")

    # Load the document
    result = load_document(test_file)

    if result:
        print("\n--- Extracted Text ---")
        print(result)
        print("\nTest SUCCESSFUL! The Document Loader is working correctly!")
    else:
        print("Test FAILED - Something went wrong")

    # Delete the test file
    os.remove(test_file)