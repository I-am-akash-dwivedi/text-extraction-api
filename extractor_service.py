from fastapi.responses import JSONResponse
from utils import extract_text_utils


def process_extraction(filename: str, content: bytes):
    response = {
        "success": False,
        "status": "error",
        "filename": filename,
        "message": "",
        "text": "",
    }

    try:
        if not content:
            return JSONResponse(
                status_code=400, content={**response, "message": "Empty file content"}
            )

        if not filename:
            return JSONResponse(
                status_code=400, content={**response, "message": "Filename is required"}
            )

        ext = filename.lower().split(".")[-1]
        if ext not in ("pdf", "docx", "txt"):
            return JSONResponse(
                status_code=400,
                content={
                    **response,
                    "message": "Unsupported file type. Only PDF, DOCX, and TXT are allowed.",
                },
            )

        text = extract_text_utils(filename, content).strip()
        return {
            **response,
            "success": True,
            "status": "success",
            "message": "File processed successfully",
            "text": text,
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={**response, "message": f"Extraction failed: {str(e)}"},
        )
