import { useState } from "react";
import { downloadFile } from "../services/api";

function getFilenameFromResponse(headers, fallbackName) {
  const disposition = headers["content-disposition"];
  if (!disposition) return fallbackName;

  const match = disposition.match(/filename="?(.*?)"?$/i);
  return match?.[1] || fallbackName;
}

export default function DownloadBox() {
  const [hash, setHash] = useState("");

  const handleDownload = async () => {
    const trimmedHash = hash.trim();
    if (!trimmedHash) return;

    try {
      const response = await downloadFile(trimmedHash);
      const fileBlobUrl = window.URL.createObjectURL(response.data);
      const filename = getFilenameFromResponse(
        response.headers,
        `download-${trimmedHash}`
      );

      const link = document.createElement("a");
      link.href = fileBlobUrl;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(fileBlobUrl);
    } catch (error) {
      const reader = new FileReader();
      reader.onload = () => {
        try {
          const payload = JSON.parse(reader.result);
          alert(payload.detail || "Unable to download file");
        } catch {
          alert("Unable to download file");
        }
      };

      if (error.response?.data instanceof Blob) {
        reader.readAsText(error.response.data);
        return;
      }

      alert("Unable to download file");
    }
  };

  return (
    <div className="card feature-card">
      <div className="card-heading">
        <span className="card-icon">GO</span>
        <div>
          <p className="card-kicker">Download</p>
          <h3>Pick up a shared file</h3>
        </div>
      </div>

      <p className="card-description">
        Paste the file hash you received and jump straight to the download in a
        new tab.
      </p>

      <label className="field">
        <span className="field-label">File hash</span>
        <input
          type="text"
          placeholder="Enter file hash"
          value={hash}
          onChange={(e) => setHash(e.target.value)}
        />
      </label>

      <button onClick={handleDownload}>Open download</button>
    </div>
  );
}
