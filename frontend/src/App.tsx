import { useState } from "react";
import NewTicketForm from "./components/NewTicketForm";
import TicketList from "./components/TicketList";
import Dashboard from "./components/Dashboard";
import "./App.css";

type Sekme = "yeni" | "talepler" | "genel";

const SAYFALAR: Record<Sekme, { baslik: string; aciklama: string }> = {
  yeni: {
    baslik: "Yeni talep",
    aciklama: "Talep otomatik sınıflandırılır; riskli olanlar onayınıza düşer.",
  },
  talepler: {
    baslik: "Talepler",
    aciklama: "Sonuçlanan tüm taleplerin kaydı.",
  },
  genel: {
    baslik: "Genel bakış",
    aciklama: "Taleplerin sonuç türüne göre dağılımı.",
  },
};

export default function App() {
  const [sekme, setSekme] = useState<Sekme>("yeni");
  const sayfa = SAYFALAR[sekme];

  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="brand">
          <img src="/favicon.svg" alt="" />
          <span>Triage</span>
        </div>

        <nav className="nav">
          {(Object.keys(SAYFALAR) as Sekme[]).map((s) => (
            <button
              key={s}
              className={`nav-item ${sekme === s ? "active" : ""}`}
              onClick={() => setSekme(s)}
            >
              {SAYFALAR[s].baslik}
            </button>
          ))}
        </nav>
      </aside>

      <main className="content">
        <header className="page-header">
          <h1>{sayfa.baslik}</h1>
          <p>{sayfa.aciklama}</p>
        </header>

        {sekme === "yeni" && <NewTicketForm />}
        {sekme === "talepler" && <TicketList />}
        {sekme === "genel" && <Dashboard />}
      </main>
    </div>
  );
}