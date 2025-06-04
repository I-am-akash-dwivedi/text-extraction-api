import os
import tempfile

import pymupdf4llm
from docx import Document


def extract_text_utils(filename: str, content: bytes):
    ext = os.path.splitext(filename)[1].lower()
    tmp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        if ext == ".pdf":
            text = pymupdf4llm.to_markdown(tmp_path)
            if not text.strip():
                raise ValueError("PyMuPDF failed to extract text")
            return text

        elif ext == ".docx":
            doc = Document(tmp_path)
            return "\n".join(para.text for para in doc.paragraphs)

        elif ext == ".txt":
            with open(tmp_path, "r", encoding="utf-8") as f:
                return f.read()

        else:
            raise ValueError(f"Unsupported file extension: {ext}")

    except Exception as e:
        raise RuntimeError(f"Failed to extract text from file '{filename}': {e}")

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
