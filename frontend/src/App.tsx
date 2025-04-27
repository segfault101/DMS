// src/App.tsx

import React, { useState, ChangeEvent, useRef } from "react";
import axios from "axios";
import ClaimTable from "./components/ClaimTable";
import AddWorkerForm from "./components/AddWorkerForm";
import AssignTraceForm from "./components/AssignTraceForm";
import AssignmentTable from "./components/AssignmentTable";

function App() {
  const [fileList, setFileList] = useState<File[]>([]);
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [refreshTrigger, setRefreshTrigger] = useState<boolean>(false); // ✅ New: refresh trigger state

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = e.target.files;
    if (selectedFiles) {
      const rmtFiles = Array.from(selectedFiles).filter(file =>
        file.name.endsWith(".rmt")
      );
      setFileList(rmtFiles);
    }
  };

  const handleUpload = async () => {
    if (fileList.length === 0) return;

    setUploading(true);

    const formData = new FormData();
    fileList.forEach((file) => {
      formData.append("files", file); // Must match FastAPI param name
    });

    try {
      await axios.post("http://localhost:8000/upload", formData);
      alert("Upload and parse successful!");
      setFileList([]);
      if (fileInputRef.current) fileInputRef.current.value = "";
      setRefreshTrigger(prev => !prev);  // ✅ Toggle to refresh claims table!
    } catch (err) {
      console.error("Upload failed:", err);
      alert("Upload failed. See console for details.");
    }

    setUploading(false);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>EDI 835 Parser Platform</h1>

      {/* Upload Section */}
      <section style={{ marginBottom: "2rem" }}>
        <h2>Upload RMT Files</h2>
        <input
          type="file"
          multiple
          //@ts-ignore
          webkitdirectory="true"
          onChange={handleFileChange}
          ref={fileInputRef}
        />
        <br /><br />
        <button
          onClick={handleUpload}
          disabled={uploading || fileList.length === 0}
        >
          {uploading ? "Uploading..." : "Upload Folder & Parse"}
        </button>
      </section>

      {/* Worker Management Section */}
      <section style={{ marginBottom: "2rem" }}>
        <AddWorkerForm />
        <AssignTraceForm />
        <AssignmentTable />
      </section>

      {/* Claims Table */}
      <section style={{ marginTop: "2rem" }}>
        <ClaimTable refreshTrigger={refreshTrigger} />  {/* ✅ Pass refresh trigger */}
      </section>
    </div>
  );
}

export default App;
