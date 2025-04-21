import csv
import os
from datetime import datetime

# Define all expected field names for the CSV
FIELDNAMES = [
    'ISA_Control_Number', 'GS_Functional_ID', 'ST_Transaction_Set_Control_Number',
    'Payment_Amount', 'Payment_Date', 'Trace_Number', 'Receiver_ID', 'Production_Date',
    'Payer_Name', 'Payer_ID', 'Payer_Contact',
    'Payee_Name', 'Payee_Tax_ID',
    'Claim_Control_Number', 'Claim_Status_Code', 'Total_Claim_Charge_Amount',
    'Claim_Payment_Amount', 'Payer_Claim_Control_Number', 'Other_Claim_ID',
    'Patient_Name', 'Corrected_Patient_Name', 'Rendering_Provider', 'Billing_Provider',
    'Service_Date', 'Adjustment_GroupCode', 'Adjustment_ReasonCode', 'Adjustment_Amount',
    'Service_Line_Code', 'Service_Line_Charge_Amount', 'Service_Line_Payment_Amount'
]

def normalize_date(edi_date):
    try:
        return datetime.strptime(edi_date, "%Y%m%d").date().isoformat()
    except Exception:
        return edi_date

def parse_edi_835_file(input_file):
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
        elif seg_id == 'NM1':
            if elements[1] == 'QC':
                current_claim['Patient_Name'] = elements[3] + ' ' + elements[4]
            elif elements[1] == '74':
                current_claim['Corrected_Patient_Name'] = elements[3] + ' ' + elements[4]
            elif elements[1] == '82' and len(elements) > 3:
                current_claim['Rendering_Provider'] = elements[3]
            elif elements[1] == 'TT':
                current_claim['Billing_Provider'] = elements[3]
        elif seg_id == 'DTM' and elements[1] in ('232', '050'):
            label = 'Service_Date' if elements[1] == '232' else 'Payment_Date'
            current_claim[label] = normalize_date(elements[2])
        elif seg_id == 'CAS':
            current_claim['Adjustment_GroupCode'] = elements[1]
            current_claim['Adjustment_ReasonCode'] = elements[2]
            current_claim['Adjustment_Amount'] = elements[3]
        elif seg_id == 'SVC':
            svc_data = {
                'Service_Line_Code': elements[1],
                'Service_Line_Charge_Amount': elements[2],
                'Service_Line_Payment_Amount': elements[3] if len(elements) > 3 else ''
            }
            row = current_claim.copy()
            row.update(svc_data)
            claims.append(row)

    return claims

def parse_directory_edi_files(input_dir, output_csv_path):
    all_rows = []
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.rmt'):
            filepath = os.path.join(input_dir, filename)
            parsed_claims = parse_edi_835_file(filepath)
            all_rows.extend(parsed_claims)

    if all_rows:
        with open(output_csv_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
            writer.writeheader()
            for row in all_rows:
                writer.writerow(row)
    else:
        print("No claims parsed")

# Example usage
#parse_directory_edi_files("C:\\Users\\Lenovo\\python_projects", "C:\\Users\\Lenovo\\python_projects\\output.csv")
parse_directory_edi_files("./input", "./output/output.csv")
