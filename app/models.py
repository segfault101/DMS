# src/app/models.py

from sqlalchemy import Column, String, Date, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, autoincrement=True)
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
    cas_info = Column(String, nullable=True)  # <<< New field to store CAS adjustments

    created_at = Column(DateTime, default=datetime.utcnow)

    note = Column(String, nullable=True)

    __table_args__ = (
        UniqueConstraint(
            "payer_claim_control_number",
            "trace_number",
            "claim_control_number",
            name="uq_claim_identity"
        ),
    )

class Worker(Base):
    __tablename__ = "workers"

    name = Column(String, primary_key=True, unique=True, nullable=False)
    assignments = relationship("WorkerAssignment", back_populates="worker", cascade="all, delete")

class WorkerAssignment(Base):
    __tablename__ = "worker_assignments"

    id = Column(String, primary_key=True)
    worker_name = Column(String, ForeignKey("workers.name", ondelete="CASCADE"), nullable=False)
    trace_number = Column(String, unique=True, nullable=False)

    worker = relationship("Worker", back_populates="assignments")
