
import os
from datetime import datetime
from sqlalchemy.orm import Session
from .models import Claim

CLAIM_STATUS_MAP = {
    "1": "Processed as primary claim",
    "2": "Processed as secondary claim",
    "3": "Processed as tertiary claim",
    "4": "Denied",
    "19": "Processed as primary, forwarded to additional payer(s)",
    "20": "Processed as secondary, forwarded to additional payer(s)",
    "21": "Processed as tertiary, forwarded to additional payer(s)",
    "22": "Reversal of previous payment",
    "23": "Not our patient",
}

def normalize_date(edi_date: str):
    try:
        return datetime.strptime(edi_date, "%Y%m%d").date()
    except Exception:
        return None

def parse_edi_835_file(input_file: str):
    with open(input_file, 'r') as f:
        edi_data = f.read()

    segments = edi_data.strip().split('~')
    claims = []

    current_claim_data = {}
    current_cas_segments = []
    current_trace_number = None

    def finalize_claim():
        if not current_claim_data:
            return None
        return Claim(
            claim_control_number=current_claim_data.get("claim_control_number"),
            claim_status_code=current_claim_data.get("claim_status_code"),
            total_claim_charge_amount=current_claim_data.get("total_claim_charge_amount"),
            claim_payment_amount=current_claim_data.get("claim_payment_amount"),
            payer_claim_control_number=current_claim_data.get("payer_claim_control_number"),
            other_claim_id=current_claim_data.get("other_claim_id"),
            payer_name=current_claim_data.get("payer_name"),
            payer_id=current_claim_data.get("payer_id"),
            payee_name=current_claim_data.get("payee_name"),
            payee_tax_id=current_claim_data.get("payee_tax_id"),
            payment_date=current_claim_data.get("payment_date"),
            trace_number=current_claim_data.get("trace_number"),
            service_date=current_claim_data.get("service_date"),
            production_date=current_claim_data.get("production_date"),
            cas_info="; ".join(current_cas_segments) if current_cas_segments else None
        )

    for segment in segments:
        elements = segment.strip().split('*')
        seg_id = elements[0]

        if seg_id == 'ISA':
            pass
        elif seg_id == 'GS':
            pass
        elif seg_id == 'ST':
            pass
        elif seg_id == 'BPR':
            current_claim_data["payment_date"] = normalize_date(elements[16])
        elif seg_id == 'TRN':
            current_trace_number = elements[2]
        elif seg_id == 'REF' and elements[1] == 'EV':
            pass
        elif seg_id == 'DTM' and elements[1] == '405':
            current_claim_data["production_date"] = normalize_date(elements[2])
        elif seg_id == 'N1' and elements[1] == 'PR':
            current_claim_data["payer_name"] = elements[2]
        elif seg_id == 'REF' and elements[1] == '2U':
            current_claim_data["payer_id"] = elements[2]
        elif seg_id == 'PER' and elements[1] == 'CX':
            pass
        elif seg_id == 'N1' and elements[1] == 'PE':
            current_claim_data["payee_name"] = elements[2]
        elif seg_id == 'REF' and elements[1] == 'TJ':
            current_claim_data["payee_tax_id"] = elements[2]
        elif seg_id == 'DTM' and elements[1] in ('232', '050'):
            label = 'service_date' if elements[1] == '232' else 'payment_date'
            current_claim_data[label] = normalize_date(elements[2])
        elif seg_id == 'CAS':
            group_code = elements[1] if len(elements) > 1 else ''
            reason_code = elements[2] if len(elements) > 2 else ''
            adjustment_amount = elements[3] if len(elements) > 3 else ''
            current_cas_segments.append(f"{group_code}:{reason_code}:{adjustment_amount}")
        elif seg_id == 'CLP':
            if "claim_control_number" in current_claim_data:
                finalized = finalize_claim()
                if finalized:
                    claims.append(finalized)
                current_claim_data = {}
                current_cas_segments = []

            raw_status = elements[2]
            meaning = CLAIM_STATUS_MAP.get(raw_status, "Unknown")
            current_claim_data["claim_status_code"] = f"{raw_status} - {meaning}"
            current_claim_data["claim_control_number"] = elements[1]
            current_claim_data["total_claim_charge_amount"] = elements[3]
            current_claim_data["claim_payment_amount"] = elements[4]
            current_claim_data["payer_claim_control_number"] = elements[7] if len(elements) > 7 else ''
            current_claim_data["other_claim_id"] = elements[9] if len(elements) > 9 else ''
            current_claim_data["trace_number"] = current_trace_number

    if "claim_control_number" in current_claim_data:
        finalized = finalize_claim()
        if finalized:
            claims.append(finalized)

    return claims

def parse_directory_edi_files(input_dir: str, db: Session):
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.rmt'):
            filepath = os.path.join(input_dir, filename)
            claims = parse_edi_835_file(filepath)
            for claim in claims:
                exists = db.query(Claim).filter_by(
                    payer_claim_control_number=claim.payer_claim_control_number,
                    trace_number=claim.trace_number,
                    claim_control_number=claim.claim_control_number
                ).first()
                if not exists:
                    db.add(claim)
    db.commit()
