#Need to have PyPDF2 installed: pip install PyPDF2
from PyPDF2 import PdfReader, PdfWriter


def is_signature_widget(annotation):
    if annotation.get("/Subtype") != "/Widget":
        return False

    current = annotation
    while current is not None:
        current = current.get_object()
        if current.get("/FT") == "/Sig":
            return True

        signature_value = current.get("/V")
        if signature_value is not None:
            signature_value = signature_value.get_object()
            if (
                hasattr(signature_value, "get")
                and signature_value.get("/ByteRange") is not None
            ):
                return True

        current = current.get("/Parent")

    return False


def remove_signature_widgets(page):
    annotations = page.get("/Annots")
    if annotations is None:
        return

    annotations = annotations.get_object()
    for index in reversed(range(len(annotations))):
        annotation = annotations[index].get_object()
        if is_signature_widget(annotation):
            del annotations[index]


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
        remove_signature_widgets(writer.pages[-1])

    # Write everything out to a brand new PDF
    with open(output_path, "wb") as outfile:
        writer.write(outfile)

print("Done! Clean file saved as:", output_path)
