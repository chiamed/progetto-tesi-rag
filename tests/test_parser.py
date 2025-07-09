from processing.parser import Parser

def test_parser_extract_text():
    parser = Parser()

    # Test with a PDF file
    pdf_text = parser.extract_text("tests/test_files/sample.pdf")
    assert pdf_text is not None, "Text should match the content of the sample PDF"

    # Test with a DOCX file
    docx_text = parser.extract_text("tests/test_files/sample.docx")
    assert docx_text is not None, "Text should match the content of the sample DOCX"

    # Test with an unsupported file type
    unsupported_text = parser.extract_text("tests/test_files/sample.txt",)
    assert unsupported_text is None
