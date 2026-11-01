
import { useEffect, useState } from "react";

import StatCard from "../components/StatCard";
import api from "../services/api";

export default function Dashboard() {
  const [summary, setSummary] = useState({
    SMS: {},
    VOICE: {},
  });

  const [company, setCompany] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadDashboard() {
      try {
        const [summaryResponse, companyResponse] =
          await Promise.all([
            api.get("/reports/summary"),
            api.get("/companies/me"),
          ]);

        setSummary(summaryResponse.data);
        setCompany(companyResponse.data);
      } catch {
        setError("Unable to load dashboard data.");
      }
    }

    loadDashboard();
  }, []);

  const count = (channel) =>
    Object.values(summary[channel] || {}).reduce(
      (total, value) => total + value,
      0
    );

  return (
    <div>
      <h2>Dashboard Overview</h2>

      {company && (
        <p>Company: {company.name}</p>
      )}

      {error && <p className="error">{error}</p>}

      <div className="stats-grid">
        <StatCard
          title="Total SMS"
          value={count("SMS")}
          icon="✉️"
          description="Recorded SMS requests"
        />

        <StatCard
          title="Total Voice Calls"
          value={count("VOICE")}
          icon="📞"
          description="Recorded voice requests"
        />

        <StatCard
          title="SMS Simulated"
          value={summary.SMS?.simulated || 0}
          icon="✓"
          description="Mock SMS results"
        />

        <StatCard
          title="Calls Simulated"
          value={summary.VOICE?.simulated || 0}
          icon="✓"
          description="Mock call results"
        />
      </div>

      <div className="dashboard-panel">
        <h3>Communication Status</h3>

        <p>
          SMS: {JSON.stringify(summary.SMS)}
        </p>

        <p>
          Voice: {JSON.stringify(summary.VOICE)}
        </p>
      </div>
    </div>
  );
}
