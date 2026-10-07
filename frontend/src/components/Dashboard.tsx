import { useState, useEffect } from "react";
import { fetchStats } from "../api";
import type { Stats } from "../types";

export default function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null);

  useEffect(() => {
    fetchStats().then((data) => setStats(data));
  }, []);

  if (!stats) return <p>Yukleniyor...</p>;

  return (
    <div className="dashboard">
      <h3>Toplam talep: {stats.toplam}</h3>
      {stats.dagilim.map((d) => {
        const yuzde = stats.toplam > 0 ? (d.adet / stats.toplam) * 100 : 0;
        return (
          <div key={d.tip} className="stat-row">
            <span>{d.tip}</span>
            <div className="bar-track">
              <div className="bar-fill" style={{ width: `${yuzde}%` }} />
            </div>
            <span>{d.adet}</span>
          </div>
        );
      })}
    </div>
  );
}