import os
import fitz  # PyMuPDF

# STEP 1
# Specify the folder containing PDFs and the output folder for images
pdf_folder = "./pdf"  # Folder containing PDF files


# STEP 2
# Iterate over all PDF files in the folder
for pdf_file in os.listdir(pdf_folder):  
    if pdf_file.endswith(".pdf"):  # Only process PDF files
        pdf_path = os.path.join(pdf_folder, pdf_file)

        # Extract the base name of the PDF without its extension
        pdf_name = os.path.splitext(pdf_file)[0]  # Extract the PDF name
        output_folder = "image/"+pdf_name  # Create a folder with the PDF name
        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True) 

        # Open the PDF
        pdf_document = fitz.open(pdf_path)

        print(f"[+] Processing PDF: {pdf_file}")

        # Iterate over PDF pages
        for page_index in range(len(pdf_document)):

            # Get the page itself
            page = pdf_document.load_page(page_index)  # Load the page
            image_list = page.get_images(full=True)  # Get images on the page

            # Printing number of images found on this page
            if image_list:
                print(f"[+] Found a total of {len(image_list)} images on page {page_index + 1}")

                for img_index, img in enumerate(image_list):
                    # Get the XREF of the image
                    xref = img[0]

                    # Extract the image bytes
                    base_image = pdf_document.extract_image(xref)
                    image_bytes = base_image["image"]

                    # Get the image extension
                    image_ext = base_image["ext"]

                    # Save the image in the output folder
                    image_name = os.path.join(
                        output_folder,
                        f"{pdf_name}_page_{page_index + 1:03d}.{image_ext}"
                    )
                    with open(image_name, "wb") as image_file:
                        image_file.write(image_bytes)
                        print(f"[+] Image saved as {image_name}")

        pdf_document.close()

print(f"All images have been saved in the folder: {output_folder}")