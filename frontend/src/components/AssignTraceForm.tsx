import React, { useState, useEffect } from "react";
import axios from "axios";

const AssignTraceForm: React.FC = () => {
  const [workerName, setWorkerName] = useState<string>("");
  const [traceNumber, setTraceNumber] = useState<string>("");
  const [workers, setWorkers] = useState<any[]>([]);
  const [error, setError] = useState<string>("");

  // Fetch workers on component mount
  useEffect(() => {
    const fetchWorkers = async () => {
      try {
        const res = await axios.get("http://localhost:8000/workers");
        setWorkers(res.data);
      } catch (err) {
        setError("Failed to load workers");
      }
    };
    fetchWorkers();
  }, []);

  // Handle assignment of trace number
  const handleAssignTraceNumber = async () => {
    if (!workerName || !traceNumber.trim()) {
      setError("Both worker name and trace number are required.");
      return;
    }

    try {
      const response = await axios.post("http://localhost:8000/assignments", {
        worker_name: workerName,
        trace_number: traceNumber,
      });
      setError("");
      setWorkerName("");
      setTraceNumber("");
      alert("Trace number assigned successfully!");
    } catch (err) {
      setError("Failed to assign trace number.");
    }
  };

  return (
    <div style={{ marginTop: "2rem" }}>
      <h2>Assign Trace Number</h2>

      <div>
        <label htmlFor="workerName">Worker Name:</label>
        <select
          id="workerName"
          value={workerName}
          onChange={(e) => setWorkerName(e.target.value)}
        >
          <option value="">Select Worker</option>
          {workers.map((worker) => (
            <option key={worker.id} value={worker.name}>
              {worker.name}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label htmlFor="traceNumber">Trace Number:</label>
        <input
          type="text"
          id="traceNumber"
          value={traceNumber}
          onChange={(e) => setTraceNumber(e.target.value)}
          placeholder="Enter trace number"
        />
      </div>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <button onClick={handleAssignTraceNumber}>Assign Trace Number</button>
    </div>
  );
};

export default AssignTraceForm;
