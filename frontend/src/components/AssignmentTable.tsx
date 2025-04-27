// src/components/AssignmentTable.tsx

import React, { useEffect, useState } from "react";
import axios from "axios";

const AssignmentTable: React.FC = () => {
  const [assignments, setAssignments] = useState<any[]>([]);

  const fetchAssignments = async () => {
    try {
      const res = await axios.get("http://localhost:8000/assignments");
      setAssignments(res.data);
    } catch (error) {
      console.error("Failed to fetch assignments:", error);
    }
  };

  useEffect(() => {
    fetchAssignments();
  }, []);

  return (
    <div style={{ marginTop: "2rem" }}>
      <h2>Assignments</h2>
      <table border={1} cellPadding={10} cellSpacing={0}>
        <thead>
          <tr>
            <th>Worker Name</th>
            <th>Trace Number</th>
          </tr>
        </thead>
        <tbody>
          {assignments.map((assignment) => (
            <tr key={assignment.id}>
              <td>{assignment.worker_name}</td>
              <td>{assignment.trace_number}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AssignmentTable;
