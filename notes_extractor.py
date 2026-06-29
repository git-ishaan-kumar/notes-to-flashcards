import os
import docx
from pypdf import PdfReader
from google.genai import types
from typing import List, Union

def extract_text_file(file_path_or_buffer) -> List[str]:
    """Extracts text from a plain TXT file path."""
    if isinstance(file_path_or_buffer, str):
        with open(file_path_or_buffer, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = file_path_or_buffer.read().decode("utf-8")
        
    return [text] if text.strip() else []

def extract_pdf_file(file_path_or_buffer) -> List[Union[str, types.Part]]:
    """Extracts text strings and images from a PDF file."""
    reader = PdfReader(file_path_or_buffer)
    contents: List[Union[str, types.Part]] = []
    page_texts = []
    
    for page in reader.pages:
        text = page.extract_text()
        if text:
            page_texts.append(text)
            
        for image_file_object in page.images:
            img_name = image_file_object.name.lower()
            mime_type = "image/jpeg" if img_name.endswith((".jpg", ".jpeg")) else "image/png"
            contents.append(types.Part.from_bytes(data=image_file_object.data, mime_type=mime_type))
            
    if page_texts:
        contents.append("\n".join(page_texts))
        
    return contents

def extract_docx_file(file_path_or_buffer) -> List[Union[str, types.Part]]:
    """Extracts text strings and images from a DOCX file."""
    doc = docx.Document(file_path_or_buffer)
    contents: List[Union[str, types.Part]] = []
    
    paragraphs_text = [p.text for p in doc.paragraphs if p.text.strip()]
    if paragraphs_text:
        contents.append("\n".join(paragraphs_text))
        
    for rel in doc.part.rels.values():
        if "image" in rel.target_ref:
            contents.append(types.Part.from_bytes(data=rel.target_part.blob, mime_type=rel.target_part.content_type))
            
    return contents

def process_document(file_input) -> List[Union[str, types.Part]]:
    """Processes a TXT, PDF, or DOCX file and returns a combined list of text and images."""
    filename = file_input if isinstance(file_input, str) else file_input.name.lower()
    
    if filename.endswith('.txt'):
        return extract_text_file(file_input)
    elif filename.endswith('.pdf'):
        return extract_pdf_file(file_input)
    elif filename.endswith('.docx'):
        return extract_docx_file(file_input)
    else:
        raise ValueError(f"Unsupported file format: {filename}")