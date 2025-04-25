import os
from typing import List

from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .database import SessionLocal, engine
from .models import Base, Claim, Worker, WorkerAssignment
from .parser import parse_directory_edi_files
from .schemas import (
    ClaimOut,
    WorkerOut,
    WorkerCreate,
    WorkerAssignmentCreate,
    WorkerAssignmentOut
)

app = FastAPI()

UPLOAD_DIR = "./input"

# Create DB tables
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- File Upload & Claim Parsing ---

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
    return {"message": "Files uploaded and claims saved to database"}

@app.get("/claims", response_model=List[ClaimOut])
def get_claims(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Claim).offset(skip).limit(limit).all()


# --- Worker Management ---

@app.post("/workers", response_model=WorkerOut)
def create_worker(worker: WorkerCreate, db: Session = Depends(get_db)):
    existing = db.query(Worker).filter_by(name=worker.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Worker already exists")
    db.add(Worker(name=worker.name))
    db.commit()
    return worker

@app.get("/workers", response_model=List[WorkerOut])
def list_workers(db: Session = Depends(get_db)):
    return db.query(Worker).all()

@app.delete("/workers", response_model=WorkerOut)
def delete_worker_by_name(name: str, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter_by(name=name).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    db.query(WorkerAssignment).filter_by(worker_name=name).delete()
    db.delete(worker)
    db.commit()
    return worker


# --- Worker Assignment ---

@app.get("/assignments", response_model=List[WorkerAssignmentOut])
def list_assignments(db: Session = Depends(get_db)):
    return db.query(WorkerAssignment).all()

@app.post("/assignments", response_model=WorkerAssignmentOut)
def assign_worker(data: WorkerAssignmentCreate, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter_by(name=data.worker_name).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    existing = db.query(WorkerAssignment).filter_by(trace_number=data.trace_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="This trace number is already assigned")

    assignment = WorkerAssignment(
        trace_number=data.trace_number,
        worker_name=data.worker_name
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment

@app.delete("/assignments")
def delete_assignment(trace_number: str = Query(...), db: Session = Depends(get_db)):
    assignment = db.query(WorkerAssignment).filter_by(trace_number=trace_number).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    db.delete(assignment)
    db.commit()
    return {"message": f"Assignment for trace number {trace_number} deleted"}
