import os
from typing import List

from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from .models import Base, Claim
from .parser import parse_directory_edi_files

from fastapi import Query
from .schemas import ClaimOut


app = FastAPI()

UPLOAD_DIR = "./input"
OUTPUT_FILE = "./output/output.csv"  # still exists temporarily

# Create all DB tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_files(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Save uploaded files
    for file in files:
        safe_filename = os.path.basename(file.filename)
        file_path = os.path.join(UPLOAD_DIR, safe_filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

    # Parse files and insert claims into DB
    parse_directory_edi_files(UPLOAD_DIR, db)

    return {"message": "Files uploaded and claims saved to database"}

@app.get("/download")
def download_csv():
    if os.path.exists(OUTPUT_FILE):
        return FileResponse(OUTPUT_FILE, media_type='text/csv', filename="output.csv")
    return {"error": "Output file not found"}


@app.get("/claims", response_model=List[ClaimOut])
def get_claims(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    claims = db.query(Claim).offset(skip).limit(limit).all()
    return claims