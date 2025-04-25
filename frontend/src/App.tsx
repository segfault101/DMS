import React, { useState } from "react";
import ClaimTable from "./components/ClaimTable";
import AddWorkerForm from "./components/AddWorkerForm";
import AssignTraceForm from "./components/AssignTraceForm";
import UploadForm from "./components/UploadForm";

function App() {
  const [refreshCounter, setRefreshCounter] = useState(0);

  const handleUploadSuccess = () => {
    setRefreshCounter((prev) => prev + 1); // Increment counter to trigger refresh
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>EDI 835 Parser Dashboard</h1>

      <UploadForm onUploadSuccess={handleUploadSuccess} />

      <hr style={{ margin: "2rem 0" }} />

      <AddWorkerForm />
      <hr style={{ margin: "2rem 0" }} />

      <AssignTraceForm />
      <hr style={{ margin: "2rem 0" }} />

      <ClaimTable refreshTrigger={refreshCounter} />
    </div>
  );
}

export default App;
