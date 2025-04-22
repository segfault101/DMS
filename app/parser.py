import os
from datetime import datetime
from sqlalchemy.orm import Session
from .models import Claim

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
    current_claim = {}

    for segment in segments:
        elements = segment.strip().split('*')
        seg_id = elements[0]

        if seg_id == 'ISA':
            current_claim['ISA_Control_Number'] = elements[13]
        elif seg_id == 'GS':
            current_claim['GS_Functional_ID'] = elements[1]
        elif seg_id == 'ST':
            current_claim['ST_Transaction_Set_Control_Number'] = elements[2]
        elif seg_id == 'BPR':
            current_claim['Payment_Amount'] = elements[2]
            current_claim['Payment_Date'] = normalize_date(elements[16])
        elif seg_id == 'TRN':
            current_claim['Trace_Number'] = elements[2]
        elif seg_id == 'REF' and elements[1] == 'EV':
            current_claim['Receiver_ID'] = elements[2]
        elif seg_id == 'DTM' and elements[1] == '405':
            current_claim['Production_Date'] = normalize_date(elements[2])
        elif seg_id == 'N1' and elements[1] == 'PR':
            current_claim['Payer_Name'] = elements[2]
        elif seg_id == 'REF' and elements[1] == '2U':
            current_claim['Payer_ID'] = elements[2]
        elif seg_id == 'PER' and elements[1] == 'CX':
            current_claim['Payer_Contact'] = elements[2]
        elif seg_id == 'N1' and elements[1] == 'PE':
            current_claim['Payee_Name'] = elements[2]
        elif seg_id == 'REF' and elements[1] == 'TJ':
            current_claim['Payee_Tax_ID'] = elements[2]
        elif seg_id == 'CLP':
            current_claim['Claim_Control_Number'] = elements[1]
            current_claim['Claim_Status_Code'] = elements[2]
            current_claim['Total_Claim_Charge_Amount'] = elements[3]
            current_claim['Claim_Payment_Amount'] = elements[4]
            current_claim['Payer_Claim_Control_Number'] = elements[7] if len(elements) > 7 else ''
            current_claim['Other_Claim_ID'] = elements[9] if len(elements) > 9 else ''
        elif seg_id == 'DTM' and elements[1] in ('232', '050'):
            label = 'Service_Date' if elements[1] == '232' else 'Payment_Date'
            current_claim[label] = normalize_date(elements[2])
        elif seg_id == 'SVC':
            # Save claim on each SVC line
            claim = Claim(
                claim_control_number=current_claim.get("Claim_Control_Number"),
                claim_status_code=current_claim.get("Claim_Status_Code"),
                total_claim_charge_amount=current_claim.get("Total_Claim_Charge_Amount"),
                claim_payment_amount=current_claim.get("Claim_Payment_Amount"),
                payer_claim_control_number=current_claim.get("Payer_Claim_Control_Number"),
                other_claim_id=current_claim.get("Other_Claim_ID"),
                payer_name=current_claim.get("Payer_Name"),
                payer_id=current_claim.get("Payer_ID"),
                payee_name=current_claim.get("Payee_Name"),
                payee_tax_id=current_claim.get("Payee_Tax_ID"),
                payment_date=current_claim.get("Payment_Date"),
                trace_number=current_claim.get("Trace_Number"),
                service_date=current_claim.get("Service_Date"),
                production_date=current_claim.get("Production_Date")
            )
            claims.append(claim)

    return claims

def parse_directory_edi_files(input_dir: str, db: Session):
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.rmt'):
            filepath = os.path.join(input_dir, filename)
            claims = parse_edi_835_file(filepath)
            db.add_all(claims)
    db.commit()
