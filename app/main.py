# src/app/main.py

import os
from typing import List

from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .database import SessionLocal, engine
from .models import Base, Claim, WorkerAssignment, Worker
from .parser import parse_directory_edi_files
from .schemas import ClaimOut, WorkerCreate, WorkerOut, WorkerAssignmentCreate, WorkerAssignmentOut, ClaimNoteUpdate

app = FastAPI()

UPLOAD_DIR = "./input"

# Create all DB tables
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CORS Middleware (still useful if you keep some separate frontends in future)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static frontend files
app.mount("/static", StaticFiles(directory="frontend/dist/assets"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("frontend/dist/index.html")

# Upload EDI files
@app.post("/upload")
async def upload_files(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    for file in files:
        safe_filename = os.path.basename(file.filename)
        file_path = os.path.join(UPLOAD_DIR, safe_filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

    parse_directory_edi_files(UPLOAD_DIR, db)
    return {"message": "Files uploaded and parsed successfully"}

# Get all claims
@app.get("/claims", response_model=List[ClaimOut])
def get_claims(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    claims = db.query(Claim).order_by(Claim.trace_number.asc()).offset(skip).limit(limit).all()
    return claims

@app.put("/claims/{claim_id}/note")
def update_claim_note(claim_id: int, data: ClaimNoteUpdate, db: Session = Depends(get_db)):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    claim.note = data.note
    db.commit()
    return {"message": "Note updated"}

# Worker Endpoints
@app.post("/workers", response_model=WorkerOut)
def create_worker(worker: WorkerCreate, db: Session = Depends(get_db)):
    new_worker = Worker(name=worker.name)
    db.add(new_worker)
    try:
        db.commit()
        db.refresh(new_worker)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Worker already exists")
    return new_worker

@app.get("/workers", response_model=List[WorkerOut])
def get_workers(db: Session = Depends(get_db)):
    return db.query(Worker).all()

@app.delete("/workers", response_model=WorkerOut)
def delete_worker(name: str, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.name == name).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    db.delete(worker)
    db.commit()
    return worker

# Assignment Endpoints
@app.post("/assignments")
def assign_worker(data: WorkerAssignmentCreate, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter_by(name=data.worker_name).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    for trace in data.trace_numbers:
        existing = db.query(WorkerAssignment).filter_by(trace_number=trace).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"Trace number {trace} already assigned")

        assignment = WorkerAssignment(
            id=str(worker.name) + "-" + trace,
            worker_name=worker.name,
            trace_number=trace
        )
        db.add(assignment)

    db.commit()
    return {"message": f"Assigned {data.worker_name} to trace numbers: {data.trace_numbers}"}

@app.get("/assignments", response_model=List[WorkerAssignmentOut])
def get_assignments(db: Session = Depends(get_db)):
    return db.query(WorkerAssignment).all()

@app.delete("/assignments")
def delete_assignment(trace_number: str = Query(...), db: Session = Depends(get_db)):
    assignment = db.query(WorkerAssignment).filter_by(trace_number=trace_number).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    db.delete(assignment)
    db.commit()
    return {"message": f"Assignment for trace number {trace_number} deleted"}
