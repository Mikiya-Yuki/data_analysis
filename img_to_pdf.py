# It recursively searches through all the folders located in the same directory as the script.
# For each folder, it compiles all the images and PDF files within that folder into a single consolidated PDF.
# The consolidated PDFs are saved in a directory named "results".
# The name of each generated PDF matches the name of the original folder from which the images and PDFs were sourced.

# run: pip3 install PyPDF2 Pillow
import os
from PIL import Image
from PyPDF2 import PdfMerger

def merge_pdfs_and_images_to_pdf(base_directory):
    # Create 'results' directory if it doesn't exist
    results_dir = os.path.join(base_directory, 'results')
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # Iterate over each folder in the base directory
    for root, dirs, files in os.walk(base_directory):
        # Skip the 'results' directory and any directory that doesn't contain any image or pdf files
        if 'results' in dirs:
            dirs.remove('results')
        if not any(file.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf')) for file in files):
            continue

        # Generate the PDF filename based on the folder name
        folder_name = os.path.basename(root)
        output_filename = os.path.join(results_dir, f"{folder_name}.pdf")

        # Create a PdfMerger object
        merger = PdfMerger()

        # Get all image files in the current directory and convert them to a single PDF
        image_files = [os.path.join(root, file) for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if image_files:
            image_files.sort()
            images = [Image.open(img_file) for img_file in image_files]
            images_rgb = [img.convert("RGB") if img.mode == "RGBA" else img for img in images]
            
            # Temporary PDF filename for the image files
            temp_pdf_filename = os.path.join(results_dir, "temp_image_pdf.pdf")
            images_rgb[0].save(temp_pdf_filename, save_all=True, append_images=images_rgb[1:])
            merger.append(temp_pdf_filename)
            os.remove(temp_pdf_filename)

        # Append existing PDF files to the merger object
        pdf_files = [os.path.join(root, file) for file in files if file.lower().endswith('.pdf')]
        for pdf_file in pdf_files:
            merger.append(pdf_file)

        # Save the merged PDF
        merger.write(output_filename)
        merger.close()

# Run the function to generate the merged PDFs
merge_pdfs_and_images_to_pdf(os.getcwd())

