import { useState } from "react";
import { detectCraters } from "../api/detect";

export default function UploadBox({ setResult }) {
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState("");
  const [status, setStatus] = useState("idle"); // idle | selected | scanning | done | error
  const [loading, setLoading] = useState(false);

  const handleUpload = (e) => {
    const selectedFile = e.target.files[0];
    if (!selectedFile) return;

    setFile(selectedFile);
    setFileName(selectedFile.name);
    setStatus("selected");
  };

  const handleSubmit = async () => {
    if (!file) return;

    setLoading(true);
    setStatus("scanning");

    try {
      const data = await detectCraters(file);
      setResult(data);
      setStatus("done");
    } catch (err) {
      console.error(err);
      setStatus("error");
    }

    setLoading(false);
  };

  return (
    <div className="upload-box">

      {/* FILE INPUT */}
      <label className="file-label">
        Choose Image
        <input type="file" accept="image/*" onChange={handleUpload} />
      </label>

      {/* STATUS */}
      <div className="status-text">
        {status === "idle" && "No image selected"}
        {status === "selected" && `Loaded: ${fileName}`}
        {status === "scanning" && "AI scanning surface..."}
        {status === "done" && "Analysis complete"}
        {status === "error" && "Processing error"}
      </div>

      {/* BUTTON */}
      <button onClick={handleSubmit} disabled={!file || loading}>
        {loading ? "Processing..." : "Run Detection"}
      </button>

      {/* AI SCAN ANIMATION */}
      {status === "scanning" && (
        <div className="ai-scan">
          <div className="scan-line"></div>
          <p>Analyzing planetary surface...</p>
        </div>
      )}

    </div>
  );
}