import { useEffect, useState } from "react";

type Health = { status: string; service: string };

const apiBase = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export default function App() {
  const [health, setHealth] = useState<Health | null>(null);
  const [apiError, setApiError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${apiBase}/health`)
      .then((response) => {
        if (!response.ok) throw new Error(`API returned ${response.status}`);
        return response.json() as Promise<Health>;
      })
      .then(setHealth)
      .catch((error: unknown) => {
        setApiError(error instanceof Error ? error.message : "Unable to reach API");
      });
  }, []);

  return (
    <main className="shell">
      <header className="topbar">
        <a className="brand" href="/" aria-label="ATR home">
          <span className="brand-mark">A</span>
          <span>AI TECHNOLOGY <strong>RESEARCH</strong></span>
        </a>
        <span className="environment">DEVELOPMENT ENVIRONMENT</span>
      </header>

      <section className="hero">
        <p className="eyebrow">ENGINEERING WORKSPACE · 2026</p>
        <h1>Build intelligent systems.<br /><span>Research with purpose.</span></h1>
        <p className="intro">
          Không gian điều phối nghiên cứu và phát triển AI, Drone và IoT.
          Nền tảng ATR đang được khởi tạo.
        </p>
      </section>

      <section className="grid" aria-label="System overview">
        <article className="panel milestone">
          <p className="panel-label">CURRENT MILESTONE</p>
          <div className="milestone-id">ATR-001</div>
          <h2>Project Foundation</h2>
          <p>Thiết lập nền tảng web, API, cơ sở dữ liệu và quy trình kiểm thử.</p>
          <div className="progress-track"><span /></div>
          <small>Foundation setup in progress</small>
        </article>

        <article className="panel">
          <p className="panel-label">SYSTEM STATUS</p>
          <div className="status-line">
            <span className={health ? "status-dot online" : "status-dot pending"} />
            <strong>{health ? "API connected" : apiError ? "API unavailable" : "Checking API…"}</strong>
          </div>
          <p className="muted">{health ? `${health.service} · ${health.status}` : apiError ?? "Đang kiểm tra kết nối đến backend."}</p>
          <div className="mini-divider" />
          <p className="panel-label">DATABASE</p>
          <strong className="database-state">PostgreSQL 16</strong>
          <p className="muted">Local container · health check enabled</p>
        </article>

        <article className="panel wide">
          <p className="panel-label">ENGINEERING DOMAINS</p>
          <div className="domains">
            <span>AI & AGENTS</span><span>DRONE / UAV</span><span>EMBEDDED</span><span>IoT SYSTEMS</span><span>HARDWARE</span><span>SOFTWARE</span>
          </div>
        </article>
      </section>

      <footer>ATR · OWNER-GOVERNED AI ENGINEERING · FOUNDATION BUILD 0.1.0</footer>
    </main>
  );
}
