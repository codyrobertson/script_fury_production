"""
Simple text extraction utilities
Handles PDF and text file processing
"""

import os
import tempfile
from typing import Optional

def extract_text_from_file(filepath: str) -> Optional[str]:
    """
    Extract text from uploaded file (PDF or text)
    
    Args:
        filepath: Path to uploaded file
        
    Returns:
        Extracted text content or None if failed
    """
    try:
        # Get file extension
        _, ext = os.path.splitext(filepath.lower())
        
        if ext == '.pdf':
            return extract_pdf_text(filepath)
        elif ext in ['.txt', '.fountain']:
            return extract_plain_text(filepath)
        else:
            # Try to read as plain text
            return extract_plain_text(filepath)
            
    except Exception as e:
        print(f"Error extracting text from {filepath}: {e}")
        return None

def extract_pdf_text(filepath: str) -> Optional[str]:
    """Extract text from PDF file"""
    try:
        import PyPDF2
        
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
            
    except ImportError:
        print("PyPDF2 not installed, trying alternative method...")
        return extract_pdf_text_alternative(filepath)
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return None

def extract_pdf_text_alternative(filepath: str) -> Optional[str]:
    """Alternative PDF text extraction using pdfplumber"""
    try:
        import pdfplumber
        
        text = ""
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        return text.strip()
        
    except ImportError:
        print("pdfplumber not installed, trying simple approach...")
        return extract_pdf_text_simple(filepath)
    except Exception as e:
        print(f"Error with pdfplumber: {e}")
        return None

def extract_pdf_text_simple(filepath: str) -> Optional[str]:
    """Simple PDF text extraction fallback"""
    try:
        # Try to use system pdftotext if available
        import subprocess
        
        result = subprocess.run(
            ['pdftotext', filepath, '-'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"pdftotext failed: {result.stderr}")
            return None
            
    except (ImportError, subprocess.TimeoutExpired, FileNotFoundError):
        print("No PDF extraction method available")
        return None

def extract_plain_text(filepath: str) -> Optional[str]:
    """Extract text from plain text file"""
    try:
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'cp1252', 'ascii']
        
        for encoding in encodings:
            try:
                with open(filepath, 'r', encoding=encoding) as file:
                    return file.read().strip()
            except UnicodeDecodeError:
                continue
        
        print(f"Could not decode text file with any encoding")
        return None
        
    except Exception as e:
        print(f"Error reading text file: {e}")
        return None

def clean_screenplay_text(text: str) -> str:
    """Clean and normalize screenplay text"""
    if not text:
        return ""
    
    # Remove excessive whitespace
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Remove trailing whitespace
        line = line.rstrip()
        
        # Keep the line (even if empty for formatting)
        cleaned_lines.append(line)
    
    # Join back together
    cleaned_text = '\n'.join(cleaned_lines)
    
    # Remove excessive blank lines (more than 2 consecutive)
    import re
    cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
    
    return cleaned_text.strip()

def estimate_pages(text: str) -> int:
    """Estimate number of screenplay pages"""
    if not text:
        return 0
    
    # Standard screenplay formatting estimates
    lines = text.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    
    # Roughly 25 lines per page in standard screenplay format
    estimated_pages = max(1, len(non_empty_lines) // 25)
    
    return estimated_pages