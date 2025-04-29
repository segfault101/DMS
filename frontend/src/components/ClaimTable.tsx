// src/components/ClaimTable.tsx
import React, { useState, useEffect } from "react";
import axios from "axios";

interface ClaimTableProps {
  refreshTrigger: boolean; // Pass a counter from parent
}

const ClaimTable: React.FC<ClaimTableProps> = ({ refreshTrigger }) => {
  const [claims, setClaims] = useState<any[]>([]);

  const fetchClaims = async () => {
    try {
      const res = await axios.get("http://localhost:8000/claims");
      setClaims(res.data);
    } catch (error) {
      console.error("Failed to fetch claims:", error);
    }
  };

  useEffect(() => {
    fetchClaims();
  }, [refreshTrigger]); // Whenever refreshTrigger changes, re-fetch

  return (
    <div style={{ marginTop: "2rem" }}>
      <h2>Parsed Claims</h2>
      <table border={1} cellPadding={5}>
        <thead>
          <tr>
            <th>Claim #</th>
            <th>Status</th>
            <th>Total Charge</th>
            <th>Payment</th>
            <th>Payer Claim #</th>
            <th>CAS Info</th>
            <th>Trace #</th>
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
              <td>{claim.cas_info || "-"}</td>
              <td>{claim.trace_number}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ClaimTable;
