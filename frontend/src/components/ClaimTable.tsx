import React, { useEffect, useState } from "react";
import axios from "axios";

interface Claim {
  id: number;
  claim_control_number?: string;
  claim_status_code?: string;
  total_claim_charge_amount?: string;
  claim_payment_amount?: string;
  payer_claim_control_number?: string;
  other_claim_id?: string;
  payer_name?: string;
  payer_id?: string;
  payee_name?: string;
  payee_tax_id?: string;
  payment_date?: string;
  trace_number?: string;
  service_date?: string;
  production_date?: string;
  created_at?: string;
}

const ClaimTable: React.FC = () => {
  const [claims, setClaims] = useState<Claim[]>([]);

  useEffect(() => {
    axios
      .get("http://localhost:8000/claims")
      .then((res) => setClaims(res.data))
      .catch((err) => console.error("Failed to fetch claims", err));
  }, []);

  return (
    <div style={{ marginTop: "2rem" }}>
      <h2>Parsed Claims</h2>
      {claims.length === 0 ? (
        <p>No claims found.</p>
      ) : (
        <table border={1} cellPadding={10} cellSpacing={0}>
          <thead>
            <tr>
              <th>Claim #</th>
              <th>Status</th>
              <th>Total Charge</th>
              <th>Payment</th>
              <th>Payer Claim #</th>
              <th>Other Claim ID</th>
              <th>Payer Name</th>
              <th>Payer ID</th>
              <th>Payee Name</th>
              <th>Payee Tax ID</th>
              <th>Payment Date</th>
              <th>Trace #</th>
              <th>Service Date</th>
              <th>Production Date</th>
              <th>Created At</th>
            </tr>
          </thead>
          <tbody>
            {claims.map((claim) => (
              <tr key={claim.id}>
                <td>{claim.claim_control_number}</td>
                <td>{claim.claim_status_code}</td>
                <td>{claim.total_claim_charge_amount}</td>
                <td>{claim.claim_payment_amount}</td>
                <td>{claim.payer_claim_control_number}</td>
                <td>{claim.other_claim_id}</td>
                <td>{claim.payer_name}</td>
                <td>{claim.payer_id}</td>
                <td>{claim.payee_name}</td>
                <td>{claim.payee_tax_id}</td>
                <td>{claim.payment_date}</td>
                <td>{claim.trace_number}</td>
                <td>{claim.service_date}</td>
                <td>{claim.production_date}</td>
                <td>{claim.created_at}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default ClaimTable;
