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
    created_at: datetime

    class Config:
        from_attributes = True


# --- Workers and Assignments ---

class WorkerBase(BaseModel):
    name: str

class WorkerCreate(WorkerBase):
    pass

class WorkerOut(WorkerBase):
    class Config:
        from_attributes = True

class WorkerAssignmentBase(BaseModel):
    trace_number: str

class WorkerAssignmentCreate(BaseModel):
    worker_name: str        # ✅ we now send worker_name (not id)
    trace_numbers: List[str]

class WorkerAssignmentOut(BaseModel):
    id: str
    trace_number: str
    worker_name: str

    class Config:
        from_attributes = True
