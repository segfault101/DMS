import React, { useState, ChangeEvent, useRef } from "react";
import axios from "axios";

function App() {
  const [fileList, setFileList] = useState<File[]>([]);
  const [uploading, setUploading] = useState(false);
  const [downloadReady, setDownloadReady] = useState(false);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = e.target.files;
    if (selectedFiles) {
      const rmtFiles = Array.from(selectedFiles).filter(file =>
        file.name.endsWith(".rmt")
      );
      setFileList(rmtFiles);
      setDownloadReady(false);
    }
  };

  const handleUpload = async () => {
    if (fileList.length === 0) return;

    setUploading(true);

    const formData = new FormData();
    fileList.forEach((file) => {
      formData.append("files", file); // must match FastAPI param name
    });

    try {
      await axios.post("http://localhost:8000/upload", formData);
      setDownloadReady(true);
      setFileList([]);
      if (fileInputRef.current) fileInputRef.current.value = "";
    } catch (err) {
      console.error("Upload failed:", err);
      alert("Upload failed. See console for details.");
    }

    setUploading(false);
  };

  const handleDownload = () => {
    window.open("http://localhost:8000/download", "_blank");
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>EDI 835 Parser</h1>

      <input
        type="file"
        multiple
        //@ts-ignore: webkitdirectory is a valid HTML attribute even if TS doesn't know it
        webkitdirectory="true"
        onChange={handleFileChange}
        ref={fileInputRef}
      />
      <br /><br />

      <button onClick={handleUpload} disabled={uploading || fileList.length === 0}>
        {uploading ? "Uploading..." : "Upload Folder & Parse"}
      </button>

      {downloadReady && (
        <>
          <br /><br />
          <button onClick={handleDownload}>Download CSV</button>
        </>
      )}
    </div>
  );
}

export default App;
