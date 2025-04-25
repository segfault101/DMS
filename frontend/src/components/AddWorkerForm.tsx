import React, { useState } from "react";
import axios from "axios";

const AddWorkerForm: React.FC = () => {
  const [workerName, setWorkerName] = useState<string>("");
  const [error, setError] = useState<string>("");

  // Handle adding a new worker
  const handleAddWorker = async () => {
    if (!workerName.trim()) {
      setError("Worker name is required.");
      return;
    }

    try {
      // Sending a POST request to add a new worker
      const response = await axios.post("http://localhost:8000/workers", {
        name: workerName,
      });
      setError("");  // Reset error message
      setWorkerName("");  // Clear the input field
      alert("Worker added successfully!");
    } catch (err) {
      setError("Failed to add worker.");
    }
  };

  return (
    <div style={{ marginTop: "2rem" }}>
      <h2>Add New Worker</h2>

      <div>
        <label htmlFor="workerName">Worker Name:</label>
        <input
          type="text"
          id="workerName"
          value={workerName}
          onChange={(e) => setWorkerName(e.target.value)}
          placeholder="Enter worker name"
        />
      </div>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <button onClick={handleAddWorker}>Add Worker</button>
    </div>
  );
};

export default AddWorkerForm;
