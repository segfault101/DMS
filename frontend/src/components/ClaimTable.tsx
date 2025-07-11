import React, { useState, useEffect } from "react";
import axios from "axios";

interface ClaimTableProps {
  refreshTrigger: boolean;
  onRefresh: () => void;
}

const workStatusOptions = [
  "",
  "in process",
  "coding review",
  "appeal done",
  "need medical records",
  "need authorization",
  "referral required",
  "insurance expired",
  "provider out of network",
];

const ClaimTable: React.FC<ClaimTableProps> = ({ refreshTrigger, onRefresh }) => {
  const [claims, setClaims] = useState<any[]>([]);
  const [notes, setNotes] = useState<{ [id: number]: string }>({});
  const [workStatuses, setWorkStatuses] = useState<{ [id: number]: string }>({});

  const fetchClaims = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/claims`);
      setClaims(res.data);

      const notesMap: { [id: number]: string } = {};
      const statusMap: { [id: number]: string } = {};

      res.data.forEach((claim: any) => {
        notesMap[claim.id] = claim.note || "";
        statusMap[claim.id] = claim.work_status || "";
      });

      setNotes(notesMap);
      setWorkStatuses(statusMap);
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

  const handleSaveWorkStatus = async (id: number) => {
    const work_status = workStatuses[id] || "";
    try {
      await axios.put(`http://localhost:8000/claims/${id}/work_status`, { work_status });
      console.log(`Saved work status for claim ${id}:`, work_status);
      onRefresh();  // ✅ trigger reload
    } catch (error) {
      console.error("Failed to save work status:", error);
    }
  };

  const [workStatusFilter, setWorkStatusFilter] = useState<string>("");


  return (
    <div style={{ marginTop: "2rem" }}>
      <h2>Parsed Claims</h2>
      <div style={{ marginBottom: "1rem" }}>
        <label htmlFor="status-filter">Filter by Work Status: </label>
        <select
          id="status-filter"
          value={workStatusFilter}
          onChange={(e) => setWorkStatusFilter(e.target.value)}
        >
          <option value="">All</option>
          {workStatusOptions.map((status) => (
            <option key={status} value={status}>
              {status || "(blank)"}
            </option>
          ))}
        </select>
      </div>
      <table border={1} cellPadding={5}>
        <thead>
          <tr>
            <th>Claim #</th>
            <th>Claim Status</th>
            <th>Total Charge</th>
            <th>Payment</th>
            <th>Payer Claim #</th>
            <th>CAS Info</th>
            <th>Trace #</th>
            <th>Notes</th>
            <th>Save Note</th>
            <th>Work Status</th>
            <th>Save Status</th>
            <th>Follow Up Deadline</th>
          </tr>
        </thead>
        <tbody>
          {claims.map((claim) => (
            <tr
              key={claim.id}
              style={{
                display:
                  workStatusFilter && claim.work_status !== workStatusFilter
                    ? "none"
                    : undefined,
              }}
            >
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
                <button onClick={() => handleSaveNote(claim.id)}>Save Note</button>
              </td>
              <td>
                <select
                  value={workStatuses[claim.id] || ""}
                  onChange={(e) =>
                    setWorkStatuses((prev) => ({
                      ...prev,
                      [claim.id]: e.target.value,
                    }))
                  }
                >
                  {workStatusOptions.map((status) => (
                    <option key={status} value={status}>
                      {status}
                    </option>
                  ))}
                </select>
              </td>
              <td>
                <button onClick={() => handleSaveWorkStatus(claim.id)}>Save Status</button>
              </td>
                <td
                  style={{
                    minWidth: "160px",
                    padding: "4px 8px",
                    whiteSpace: "nowrap",
                    backgroundColor:
                      claim.follow_up &&
                      new Date(claim.follow_up) < new Date(Date.now() - 20 * 24 * 60 * 60 * 1000)
                        ? "#f8d7da"
                        : "transparent",
                  }}
                >
                  {claim.follow_up ? new Date(claim.follow_up).toLocaleString() : "-"}
                </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ClaimTable;
