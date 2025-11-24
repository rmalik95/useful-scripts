#Need to have PyPDF2 installed: pip install PyPDF2
from PyPDF2 import PdfReader, PdfWriter

#Add the source path of the directory with the docoument name
input_path = "Document.pdf"
output_path = "Document_Cleaned.pdf"

# Open the original PDF in read-binary mode
with open(input_path, "rb") as infile:
    reader = PdfReader(infile)

    # If the PDF is actually password-protected, you'd need:
    # reader.decrypt("your_password_here")

    writer = PdfWriter()

    # Copy each page into a new writer
    for page in reader.pages:
        writer.add_page(page)

    # Write everything out to a brand new PDF
    with open(output_path, "wb") as outfile:
        writer.write(outfile)

print("Done! Clean file saved as:", output_path)
