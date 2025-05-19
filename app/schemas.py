# src/app/schemas.py

from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel

# --- Claims ---

class ClaimOut(BaseModel):
    id: int
    claim_control_number: Optional[str] = None
    claim_status_code: Optional[str] = None
    total_claim_charge_amount: Optional[str] = None
    claim_payment_amount: Optional[str] = None
    payer_claim_control_number: Optional[str] = None
    other_claim_id: Optional[str] = None
    payer_name: Optional[str] = None
    payer_id: Optional[str] = None
    payee_name: Optional[str] = None
    payee_tax_id: Optional[str] = None
    payment_date: Optional[date] = None
    trace_number: Optional[str] = None
    service_date: Optional[date] = None
    production_date: Optional[date] = None
    cas_info: Optional[str] = None
    created_at: datetime
    note: Optional[str] = None
    work_status: Optional[str] = None
    follow_up: Optional[datetime] = None

    class Config:
        from_attributes = True

class ClaimNoteUpdate(BaseModel):
    note: str

class ClaimWorkStatusUpdate(BaseModel):
    work_status: str


# --- Workers and Assignments ---

class WorkerBase(BaseModel):
    name: str

class WorkerCreate(WorkerBase):
    pass

class WorkerOut(WorkerBase):
    class Config:
        from_attributes = True

class WorkerAssignmentBase(BaseModel):
    claim_control_number: str

class WorkerAssignmentCreate(BaseModel):
    worker_name: str
    claim_control_numbers: List[str]

class WorkerAssignmentOut(BaseModel):
    id: str
    worker_name: str
    claim_control_number: str

    class Config:
        from_attributes = True
