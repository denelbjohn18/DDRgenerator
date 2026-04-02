import os
import fitz  # PyMuPDF
from PIL import Image
import io

def extract_content(pdf_path, temp_images_dir="temp_images/"):
    """
    Extracts text and images from a given PDF file.
    Saves extracted images to temp_images_dir.
    Returns the full text and a list of paths to the extracted images.
    """
    if not os.path.exists(temp_images_dir):
        os.makedirs(temp_images_dir, exist_ok=True)
    
    text_content = []
    image_paths = []
    
    # Generate a unique prefix based on the filename to avoid collisions
    file_prefix = os.path.splitext(os.path.basename(pdf_path))[0]
    
    doc = fitz.open(pdf_path)
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # Extract text
        text = page.get_text()
        if text:
            text_content.append(text)
            
        # Extract images
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # Save the image
            image_filename = f"{file_prefix}_page{page_num+1}_img{img_index+1}.{image_ext}"
            image_filepath = os.path.join(temp_images_dir, image_filename)
            
            try:
                # Open with PIL and save to ensure valid format and possibly normalize
                image = Image.open(io.BytesIO(image_bytes))
                
                # Convert to RGB if it's CMYK or RGBA to avoid PDF insertion issues later
                if image.mode in ("RGBA", "CMYK", "P"):
                    image = image.convert("RGB")
                    
                # Save as PNG typically ensures broader compatibility for reportlab later
                final_filename = f"{file_prefix}_page{page_num+1}_img{img_index+1}.png"
                final_filepath = os.path.join(temp_images_dir, final_filename)
                
                image.save(final_filepath, "PNG")
                image_paths.append(final_filepath)
            except Exception as e:
                print(f"Failed to process image {image_filename}: {e}")
                
    doc.close()
    
    return "\n".join(text_content), image_paths

def process_uploaded_file(uploaded_file, save_dir="temp_pdfs"):
    """
    Saves an uploaded Streamlit file to a temporary location to pass to PyMuPDF.
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
        
    file_path = os.path.join(save_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    return file_path
