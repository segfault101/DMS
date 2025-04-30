import React, { useState, useEffect } from "react";
import axios from "axios";

interface ClaimTableProps {
  refreshTrigger: boolean;
}

const ClaimTable: React.FC<ClaimTableProps> = ({ refreshTrigger }) => {
  const [claims, setClaims] = useState<any[]>([]);
  const [notes, setNotes] = useState<{ [id: number]: string }>({});

  const fetchClaims = async () => {
    try {
      const res = await axios.get("http://localhost:8000/claims");
      setClaims(res.data);

      // ✅ Initialize notes from API response
      const notesMap: { [id: number]: string } = {};
      res.data.forEach((claim: any) => {
        notesMap[claim.id] = claim.note || "";
      });
      setNotes(notesMap);
    } catch (error) {
      console.error("Failed to fetch claims:", error);
    }
  };

  useEffect(() => {
    fetchClaims();
  }, [refreshTrigger]);

  const handleNoteChange = (id: number, value: string) => {
    setNotes((prev) => ({ ...prev, [id]: value }));
  };

  const handleSaveNote = async (id: number) => {
    const note = notes[id] || "";
    try {
      await axios.put(`http://localhost:8000/claims/${id}/note`, { note });
      console.log(`Saved note for claim ${id}:`, note);
    } catch (error) {
      console.error("Failed to save note:", error);
    }
  };

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
            <th>Notes</th>
            <th>Action</th>
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
              <td>
                <input
                  type="text"
                  value={notes[claim.id] || ""}
                  onChange={(e) => handleNoteChange(claim.id, e.target.value)}
                />
              </td>
              <td>
                <button onClick={() => handleSaveNote(claim.id)}>Save</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ClaimTable;
