// src/components/AddWorkerForm.tsx

import React, { useState, useEffect } from "react";
import axios from "axios";

const AddWorkerForm: React.FC = () => {
  const [name, setName] = useState("");
  const [workers, setWorkers] = useState<any[]>([]);

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

  const handleAddWorker = async () => {
    if (!name.trim()) {
      alert("Please enter a valid worker name.");
      return;
    }

    const payload = {
      name: name.trim(), // ✅ Sending just the worker name
    };

    try {
      await axios.post("http://localhost:8000/workers", payload);
      alert(`Worker '${name}' added successfully!`);
      setName("");
      fetchWorkers(); // Refresh list
    } catch (error) {
      console.error(error);
      alert("Failed to add worker.");
    }
  };

  return (
    <div style={{ marginBottom: "2rem" }}>
      <h2>Add Worker</h2>

      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Enter worker name"
        style={{ width: "300px", marginRight: "1rem" }}
      />

      <button onClick={handleAddWorker}>Add Worker</button>

      {/* Show current workers */}
      <div style={{ marginTop: "1rem" }}>
        <h3>Current Workers</h3>
        <ul>
          {workers.map((worker) => (
            <li key={worker.name}>{worker.name}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default AddWorkerForm;
