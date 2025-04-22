from datetime import date, datetime
from pydantic import BaseModel

class ClaimOut(BaseModel):
    id: int
    claim_control_number: str | None = None
    claim_status_code: str | None = None
    total_claim_charge_amount: str | None = None
    claim_payment_amount: str | None = None
    payer_claim_control_number: str | None = None
    other_claim_id: str | None = None
    payer_name: str | None = None
    payer_id: str | None = None
    payee_name: str | None = None
    payee_tax_id: str | None = None
    payment_date: date | None = None
    trace_number: str | None = None
    service_date: date | None = None
    production_date: date | None = None
    created_at: datetime

    class Config:
        orm_mode = True  # allows SQLAlchemy model to be converted to Pydantic
