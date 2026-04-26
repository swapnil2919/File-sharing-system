import UploadBox from "../components/UploadBox";
import DownloadBox from "../components/DownloadBox";
import "../styles/main.css";

function SpiderLogo() {
  return (
    <svg
      className="brand-logo"
      viewBox="0 0 120 120"
      aria-hidden="true"
      role="img"
    >
      <defs>
        <linearGradient id="spiderShell" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#101729" />
          <stop offset="100%" stopColor="#db1f48" />
        </linearGradient>
      </defs>
      <g fill="none" strokeLinecap="round" strokeLinejoin="round">
        <path
          d="M36 34 14 18M31 49 8 44M31 66 10 73M39 82 18 98M84 34l22-16M89 49l23-5M89 66l21 7M81 82l21 16"
          stroke="#ff7a59"
          strokeWidth="6"
        />
        <path
          d="M60 20c11 0 20 9 20 20S71 60 60 60 40 51 40 40s9-20 20-20Zm0 35c16 0 29 14 29 31 0 8-13 14-29 14S31 94 31 86c0-17 13-31 29-31Z"
          fill="url(#spiderShell)"
          stroke="#f2f5ff"
          strokeWidth="4"
        />
        <circle cx="52" cy="38" r="4" fill="#f2f5ff" />
        <circle cx="68" cy="38" r="4" fill="#f2f5ff" />
        <path d="M53 47c3 3 11 3 14 0" stroke="#f2f5ff" strokeWidth="4" />
      </g>
    </svg>
  );
}

export default function Home() {
  return (
    <main className="page-shell">
      <div className="ambient ambient-left" />
      <div className="ambient ambient-right" />

      <section className="hero-panel">
        <div className="brand-pill">
          <SpiderLogo />
          <span>Spider Sharing</span>
        </div>

        <div className="hero-copy">
          <p className="eyebrow">Fast. private. link-based transfer.</p>
          <h1>Share files through a sleek web with Spider Sharing.</h1>
          <p className="hero-text">
            Upload securely, control file expiry, and pass around clean
            download links from one modern dashboard.
          </p>
        </div>

        <div className="hero-stats">
          <div className="stat-card">
            <strong>7 days</strong>
            <span>Flexible expiry window</span>
          </div>
          <div className="stat-card">
            <strong>1 click</strong>
            <span>Instant download links</span>
          </div>
          <div className="stat-card">
            <strong>Private</strong>
            <span>One-time access supported</span>
          </div>
        </div>
      </section>

      <section className="workspace-grid">
        <UploadBox />
        <DownloadBox />
      </section>
    </main>
  );
}
