import base64

from auth import get_api_key
from extractor_service import process_extraction
from fastapi import Depends, FastAPI, File, Header, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(
    title="Text Extraction API",
    version="1.0.0",
    description="API for extracting text from various file formats.",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/")
async def root():
    return {"status": "success", "message": "Text Extraction API"}


@app.api_route("/health", methods=["GET", "HEAD"])
async def health_check():
    return {"status": "success", "message": "API is up and running"}


class Base64Request(BaseModel):
    filename: str
    filedata: str


@app.post("/extract/upload")
async def extract_from_file(
    file: UploadFile = File(...), api_key: str = Depends(get_api_key)
):
    content = await file.read()
    return process_extraction(file.filename or "", content)


@app.post("/extract/base64")
async def extract_from_base64(
    payload: Base64Request, api_key: str = Depends(get_api_key)
):
    try:
        content = base64.b64decode(payload.filedata)
    except Exception:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "status": "error",
                "filename": payload.filename,
                "message": "Invalid base64 encoding",
                "text": "",
            },
        )

    return process_extraction(payload.filename, content)
