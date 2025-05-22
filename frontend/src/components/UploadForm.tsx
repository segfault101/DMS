// src/components/UploadForm.tsx
import React, { useRef, useState, ChangeEvent } from "react";
import axios from "axios";

interface UploadFormProps {
  onUploadSuccess: () => void;
}

const UploadForm: React.FC<UploadFormProps> = ({ onUploadSuccess }) => {
  const [fileList, setFileList] = useState<File[]>([]);
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

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
    fileList.forEach(file => {
      formData.append("files", file);
    });

    try {
      await axios.post(`${import.meta.env.VITE_API_BASE_URL}/upload`, formData);
      alert("Files uploaded and parsed successfully!");
      setFileList([]);
      if (fileInputRef.current) fileInputRef.current.value = "";
      onUploadSuccess(); // ← Fire refresh callback
    } catch (err) {
      console.error("Upload failed:", err);
      alert("Upload failed. Check console for details.");
    }

    setUploading(false);
  };

  return (
    <div style={{ marginTop: "2rem" }}>
      <h2>Upload .rmt Files</h2>
      <input
        type="file"
        multiple
        onChange={handleFileChange}
        ref={fileInputRef}
        style={{ marginBottom: "1rem" }}
      />
      <br />
      <button onClick={handleUpload} disabled={uploading || fileList.length === 0}>
        {uploading ? "Uploading..." : "Upload"}
      </button>
    </div>
  );
};

export default UploadForm;
