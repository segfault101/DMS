import React, { useState, useEffect } from "react";
import axios from "axios";

const AssignClaimForm: React.FC = () => {
  const [workers, setWorkers] = useState<any[]>([]);
  const [selectedWorkerName, setSelectedWorkerName] = useState<string>("");
  const [claimControlNumber, setClaimControlNumber] = useState<string>("");

  useEffect(() => {
    const fetchWorkers = async () => {
      try {
        const res = await axios.get("http://localhost:8000/workers");
        setWorkers(res.data);
      } catch (error) {
        console.error("Failed to fetch workers:", error);
      }
    };
    fetchWorkers();
  }, []);

  const handleAssign = async () => {
    const trimmed = claimControlNumber.trim();
    if (!selectedWorkerName || !trimmed) {
      alert("Please select a worker and enter a claim control number.");
      return;
    }

    const payload = {
      worker_name: selectedWorkerName,
      claim_control_numbers: [trimmed],
    };

    try {
      await axios.post("http://localhost:8000/assignments", payload);
      alert(`Assigned claim ${trimmed} to ${selectedWorkerName} successfully!`);
      setClaimControlNumber("");
      setSelectedWorkerName("");
    } catch (error) {
      console.error(error);
      alert("Failed to assign claim.");
    }
  };

  return (
    <div style={{ marginTop: "2rem" }}>
      <h2>Assign Claim</h2>

      <select
        value={selectedWorkerName}
        onChange={(e) => setSelectedWorkerName(e.target.value)}
      >
        <option value="">Select a worker</option>
        {workers.map((worker) => (
          <option key={worker.name} value={worker.name}>
            {worker.name}
          </option>
        ))}
      </select>

      <input
        type="text"
        value={claimControlNumber}
        onChange={(e) => setClaimControlNumber(e.target.value)}
        placeholder="Enter claim control number"
        style={{ marginLeft: "1rem", width: "220px" }}
      />

      <button
        onClick={handleAssign}
        style={{ marginLeft: "1rem" }}
        disabled={!selectedWorkerName || !claimControlNumber.trim()}
      >
        Assign
      </button>
    </div>
  );
};

export default AssignClaimForm;
