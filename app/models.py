from sqlalchemy import Column, Integer, String, Date, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)

    claim_control_number = Column(String)
    claim_status_code = Column(String)
    total_claim_charge_amount = Column(String)
    claim_payment_amount = Column(String)
    payer_claim_control_number = Column(String)
    other_claim_id = Column(String)

    payer_name = Column(String)
    payer_id = Column(String)
    payee_name = Column(String)
    payee_tax_id = Column(String)

    payment_date = Column(Date)
    trace_number = Column(String)
    service_date = Column(Date)
    production_date = Column(Date)

    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint(
            "payer_claim_control_number",
            "trace_number",
            "claim_control_number",
            name="uq_claim_identity"
        ),
    )
