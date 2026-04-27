import { useState } from "react";
import { API_BASE_URL, uploadFile } from "../services/api";

export default function UploadBox() {
  const [file, setFile] = useState(null);
  const [days, setDays] = useState("");
  const [oneTime, setOneTime] = useState(false);
  const [result, setResult] = useState(null);

  const handleUpload = async () => {
    if (!file) return alert("Select file");

    const formData = new FormData();
    formData.append("file", file);
    if (days) formData.append("days", days);
    formData.append("one_time", oneTime);

    try {
      const res = await uploadFile(formData);
      setResult(res.data);
    } catch (err) {
      alert("Upload failed");
    }
  };

  const resolvedDownloadUrl = result?.download_url?.startsWith("http")
    ? result.download_url
    : `${API_BASE_URL}${result?.download_url || ""}`;

  const copyToClipboard = async (value) => {
    try {
      await navigator.clipboard.writeText(value);
    } catch (err) {
      alert("Copy failed. Please copy it manually.");
    }
  };

  return (
    <div className="card feature-card">
      <div className="card-heading">
        <span className="card-icon">UP</span>
        <div>
          <p className="card-kicker">Upload</p>
          <h3>Drop a file into the web</h3>
        </div>
      </div>

      <p className="card-description">
        Choose a file, set how long it stays available, and generate a secure
        shareable link.
      </p>

      <label className="field">
        <span className="field-label">Choose file</span>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      </label>

      <label className="field">
        <span className="field-label">Expiry in days</span>
        <input
          type="number"
          placeholder="Days (max 7)"
          value={days}
          onChange={(e) => setDays(e.target.value)}
        />
      </label>

      <label className="checkbox-row">
        <input
          type="checkbox"
          checked={oneTime}
          onChange={() => setOneTime(!oneTime)}
        />
        <span>Allow one-time download only</span>
      </label>

      <button onClick={handleUpload}>Create share link</button>

      {result && (
        <div className="result">
          <p className="result-title">Share details ready</p>

          <div className="result-block">
            <span className="result-label">Download URL</span>
            <code>{resolvedDownloadUrl}</code>
            <div className="result-actions">
              <button
                type="button"
                className="secondary-button"
                onClick={() => copyToClipboard(resolvedDownloadUrl)}
              >
                Copy URL
              </button>
              <a href={resolvedDownloadUrl} target="_blank" rel="noreferrer">
                Open link
              </a>
            </div>
          </div>

          <div className="result-block">
            <span className="result-label">Hash</span>
            <code>{result.file_hash}</code>
            <div className="result-actions">
              <button
                type="button"
                className="secondary-button"
                onClick={() => copyToClipboard(result.file_hash)}
              >
                Copy hash
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
