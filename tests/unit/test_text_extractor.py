"""
Unit tests for text_extractor.py
"""

import unittest
import tempfile
import os
from unittest.mock import patch, mock_open, MagicMock
import sys

# Add the parent directory to sys.path to import utils
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.text_extractor import (
    extract_text_from_file,
    extract_plain_text,
    extract_pdf_text,
    extract_pdf_text_alternative,
    extract_pdf_text_simple,
    clean_screenplay_text,
    estimate_pages
)


class TestTextExtractor(unittest.TestCase):
    """Test cases for text extraction utilities"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_text = "FADE IN:\n\nEXT. CITY STREET - DAY\n\nA bustling urban scene."
        self.test_dir = os.path.join(os.path.dirname(__file__), '..', 'fixtures')
        self.sample_file = os.path.join(self.test_dir, 'sample_screenplay.txt')

    def test_extract_plain_text_success(self):
        """Test successful plain text extraction"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(self.test_text)
            temp_path = f.name

        try:
            result = extract_plain_text(temp_path)
            self.assertEqual(result, self.test_text)
        finally:
            os.unlink(temp_path)

    def test_extract_plain_text_with_encoding(self):
        """Test plain text extraction with different encodings"""
        # Test with UTF-8
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write("Test with UTF-8: café")
            temp_path = f.name

        try:
            result = extract_plain_text(temp_path)
            self.assertIn("café", result)
        finally:
            os.unlink(temp_path)

    def test_extract_plain_text_file_not_found(self):
        """Test plain text extraction with non-existent file"""
        result = extract_plain_text("/nonexistent/file.txt")
        self.assertIsNone(result)

    def test_extract_plain_text_empty_file(self):
        """Test plain text extraction with empty file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("")
            temp_path = f.name

        try:
            result = extract_plain_text(temp_path)
            self.assertEqual(result, "")
        finally:
            os.unlink(temp_path)

    @unittest.skip("PDF functionality not implemented in simple version")
    @patch('utils.text_extractor.PyPDF2')
    def test_extract_pdf_text_success(self, mock_pypdf2):
        """Test successful PDF text extraction with PyPDF2"""
        # Mock PyPDF2 components
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Page 1 text"
        
        mock_reader = MagicMock()
        mock_reader.pages = [mock_page]
        
        mock_pypdf2.PdfReader.return_value = mock_reader

        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            temp_path = f.name

        try:
            result = extract_pdf_text(temp_path)
            self.assertEqual(result, "Page 1 text")
        finally:
            os.unlink(temp_path)

    @unittest.skip("PDF functionality not implemented in simple version")
    @patch('utils.text_extractor.PyPDF2')
    def test_extract_pdf_text_import_error(self, mock_pypdf2):
        """Test PDF text extraction when PyPDF2 is not available"""
        mock_pypdf2.side_effect = ImportError("PyPDF2 not installed")

        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            temp_path = f.name

        try:
            with patch('utils.text_extractor.extract_pdf_text_alternative') as mock_alt:
                mock_alt.return_value = "Alternative extraction"
                result = extract_pdf_text(temp_path)
                self.assertEqual(result, "Alternative extraction")
        finally:
            os.unlink(temp_path)

    @unittest.skip("PDF functionality not implemented in simple version")
    @patch('utils.text_extractor.pdfplumber')
    def test_extract_pdf_text_alternative_success(self, mock_pdfplumber):
        """Test alternative PDF text extraction with pdfplumber"""
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Page text"
        
        mock_pdf = MagicMock()
        mock_pdf.pages = [mock_page]
        mock_pdf.__enter__ = MagicMock(return_value=mock_pdf)
        mock_pdf.__exit__ = MagicMock(return_value=None)
        
        mock_pdfplumber.open.return_value = mock_pdf

        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            temp_path = f.name

        try:
            result = extract_pdf_text_alternative(temp_path)
            self.assertEqual(result, "Page text")
        finally:
            os.unlink(temp_path)

    @unittest.skip("PDF functionality not implemented in simple version")
    @patch('utils.text_extractor.subprocess.run')
    def test_extract_pdf_text_simple_success(self, mock_run):
        """Test simple PDF text extraction with pdftotext"""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="PDF text content"
        )

        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            temp_path = f.name

        try:
            result = extract_pdf_text_simple(temp_path)
            self.assertEqual(result, "PDF text content")
        finally:
            os.unlink(temp_path)

    @unittest.skip("PDF functionality not implemented in simple version")
    @patch('utils.text_extractor.subprocess.run')
    def test_extract_pdf_text_simple_failure(self, mock_run):
        """Test simple PDF text extraction failure"""
        mock_run.return_value = MagicMock(
            returncode=1,
            stderr="Error message"
        )

        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            temp_path = f.name

        try:
            result = extract_pdf_text_simple(temp_path)
            self.assertIsNone(result)
        finally:
            os.unlink(temp_path)

    def test_extract_text_from_file_txt(self):
        """Test extract_text_from_file with .txt file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(self.test_text)
            temp_path = f.name

        try:
            result = extract_text_from_file(temp_path)
            self.assertEqual(result, self.test_text)
        finally:
            os.unlink(temp_path)

    def test_extract_text_from_file_fountain(self):
        """Test extract_text_from_file with .fountain file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.fountain', delete=False) as f:
            f.write(self.test_text)
            temp_path = f.name

        try:
            result = extract_text_from_file(temp_path)
            self.assertEqual(result, self.test_text)
        finally:
            os.unlink(temp_path)

    def test_extract_text_from_file_unknown_extension(self):
        """Test extract_text_from_file with unknown extension"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.unknown', delete=False) as f:
            f.write(self.test_text)
            temp_path = f.name

        try:
            result = extract_text_from_file(temp_path)
            self.assertEqual(result, self.test_text)  # Should fall back to plain text
        finally:
            os.unlink(temp_path)

    def test_clean_screenplay_text_empty(self):
        """Test clean_screenplay_text with empty input"""
        result = clean_screenplay_text("")
        self.assertEqual(result, "")

    def test_clean_screenplay_text_none(self):
        """Test clean_screenplay_text with None input"""
        result = clean_screenplay_text(None)
        self.assertEqual(result, "")

    def test_clean_screenplay_text_whitespace(self):
        """Test clean_screenplay_text removes excessive whitespace"""
        messy_text = "Line 1   \n\n\n\nLine 2\n\n\n\n\nLine 3   "
        result = clean_screenplay_text(messy_text)
        
        # Should remove excessive blank lines and trailing spaces
        self.assertNotIn("   ", result)
        self.assertNotIn("\n\n\n", result)
        self.assertIn("Line 1", result)
        self.assertIn("Line 2", result)
        self.assertIn("Line 3", result)

    def test_clean_screenplay_text_preserve_format(self):
        """Test clean_screenplay_text preserves screenplay formatting"""
        screenplay_text = "FADE IN:\n\nEXT. LOCATION - DAY\n\nAction line."
        result = clean_screenplay_text(screenplay_text)
        
        # Should preserve the double line breaks for screenplay format
        self.assertIn("FADE IN:", result)
        self.assertIn("EXT. LOCATION - DAY", result)
        self.assertIn("Action line.", result)

    def test_estimate_pages_empty(self):
        """Test estimate_pages with empty text"""
        result = estimate_pages("")
        self.assertEqual(result, 0)

    def test_estimate_pages_none(self):
        """Test estimate_pages with None"""
        result = estimate_pages(None)
        self.assertEqual(result, 0)

    def test_estimate_pages_short_text(self):
        """Test estimate_pages with short text"""
        short_text = "This is a short text."
        result = estimate_pages(short_text)
        self.assertEqual(result, 1)  # Minimum 1 page

    def test_estimate_pages_long_text(self):
        """Test estimate_pages with long text"""
        # Create text with 50 lines (should be ~2 pages)
        lines = ["Line " + str(i) for i in range(1, 51)]
        long_text = "\n".join(lines)
        result = estimate_pages(long_text)
        self.assertEqual(result, 2)

    def test_estimate_pages_with_empty_lines(self):
        """Test estimate_pages ignores empty lines"""
        text_with_empty_lines = "Line 1\n\n\nLine 2\n\n\n\nLine 3"
        result = estimate_pages(text_with_empty_lines)
        self.assertEqual(result, 1)  # Only 3 non-empty lines

    def test_extract_text_from_file_with_fixture(self):
        """Test extract_text_from_file with actual fixture file"""
        if os.path.exists(self.sample_file):
            result = extract_text_from_file(self.sample_file)
            self.assertIsNotNone(result)
            self.assertIn("THE TEST SCREENPLAY", result)
            self.assertIn("FADE IN:", result)
            self.assertIn("JOHN", result)
            self.assertIn("SARAH", result)

    def test_extract_text_from_file_nonexistent(self):
        """Test extract_text_from_file with nonexistent file"""
        result = extract_text_from_file("/nonexistent/file.txt")
        self.assertIsNone(result)


class TestTextExtractorIntegration(unittest.TestCase):
    """Integration tests for text extractor with real files"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = os.path.join(os.path.dirname(__file__), '..', 'fixtures')

    def test_extract_sample_screenplay(self):
        """Test extracting sample screenplay"""
        sample_file = os.path.join(self.test_dir, 'sample_screenplay.txt')
        if os.path.exists(sample_file):
            text = extract_text_from_file(sample_file)
            self.assertIsNotNone(text)
            
            # Check for expected content
            self.assertIn("THE TEST SCREENPLAY", text)
            self.assertIn("FADE IN:", text)
            self.assertIn("EXT. CITY STREET - DAY", text)
            self.assertIn("INT. COFFEE SHOP - CONTINUOUS", text)
            self.assertIn("JOHN", text)
            self.assertIn("SARAH", text)

    def test_extract_malformed_screenplay(self):
        """Test extracting malformed screenplay"""
        malformed_file = os.path.join(self.test_dir, 'malformed_screenplay.txt')
        if os.path.exists(malformed_file):
            text = extract_text_from_file(malformed_file)
            self.assertIsNotNone(text)
            
            # Should still extract text even if format is wrong
            self.assertIn("This is not a proper screenplay format", text)

    def test_extract_large_screenplay(self):
        """Test extracting large screenplay"""
        large_file = os.path.join(self.test_dir, 'large_screenplay.txt')
        if os.path.exists(large_file):
            text = extract_text_from_file(large_file)
            self.assertIsNotNone(text)
            
            # Check for expected content
            self.assertIn("LARGE SCREENPLAY TEST", text)
            self.assertIn("ALEX", text)
            self.assertIn("MAYA", text)
            
            # Should be estimated as multiple pages
            pages = estimate_pages(text)
            self.assertGreater(pages, 1)


if __name__ == '__main__':
    unittest.main()