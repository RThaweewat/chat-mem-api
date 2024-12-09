from io import BytesIO
from unittest.mock import patch

import pytest
from fastapi import UploadFile

from src.services.document_loader import process_and_store_docs


@pytest.fixture
def mock_pdf_file():
    file_content = b"Dummy PDF content"
    return UploadFile(filename="test.pdf", file=BytesIO(file_content))


@patch("src.services.document_loader.textract.process")
@patch("src.services.document_loader.vectorstore")
def test_process_and_store_docs(mock_vectorstore, mock_textract, mock_pdf_file):
    # Mock textract response
    mock_textract.return_value = b"Extracted text from PDF."

    # Process file
    result = process_and_store_docs([mock_pdf_file])

    assert len(result) == 1
    assert result[0]["filename"] == "test.pdf"
    mock_vectorstore.add_documents.assert_called_once()
