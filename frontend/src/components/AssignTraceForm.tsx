// src/components/AssignTraceForm.tsx

import React, { useState, useEffect } from "react";
import axios from "axios";

const AssignTraceForm: React.FC = () => {
  const [workers, setWorkers] = useState<any[]>([]);
  const [selectedWorkerName, setSelectedWorkerName] = useState<string>("");
  const [traceNumber, setTraceNumber] = useState("");

  const fetchWorkers = async () => {
    try {
      const res = await axios.get("http://localhost:8000/workers");
      setWorkers(res.data);
    } catch (error) {
      console.error("Failed to fetch workers:", error);
    }
  };

  useEffect(() => {
    fetchWorkers();
  }, []);

  const handleAssign = async () => {
    if (!selectedWorkerName || !traceNumber.trim()) {
      alert("Please select a worker and enter a trace number.");
      return;
    }

    const payload = {
      worker_name: selectedWorkerName,               // ✅ send worker_name now
      trace_numbers: [traceNumber.trim()],
    };

    try {
      await axios.post("http://localhost:8000/assignments", payload);
      alert(`Assigned trace number to ${selectedWorkerName} successfully!`);
      setTraceNumber("");
      setSelectedWorkerName("");
    } catch (error) {
      console.error(error);
      alert("Failed to assign trace number.");
    }
  };

  return (
    <div style={{ marginTop: "2rem" }}>
      <h2>Assign Trace Number</h2>

      {/* Dropdown to select worker */}
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

      {/* Input for trace number */}
      <input
        value={traceNumber}
        onChange={(e) => setTraceNumber(e.target.value)}
        placeholder="Enter trace number"
        style={{ marginLeft: "1rem", width: "300px" }}
      />

      <button
        onClick={handleAssign}
        style={{ marginLeft: "1rem" }}
        disabled={!selectedWorkerName || !traceNumber.trim()}
      >
        Assign
      </button>
    </div>
  );
};

export default AssignTraceForm;
