import { useState } from "react";
import NewTicketForm from "./components/NewTicketForm";
import TicketList from "./components/TicketList";
import Dashboard from "./components/Dashboard";
import "./App.css";

type Sekme = "yeni" | "biletler" | "dashboard";

export default function App() {
  const [sekme, setSekme] = useState<Sekme>("yeni");

  return (
    <div className="app">
      <header>
        <h1>Support Triage Agent</h1>
        <nav>
          <button onClick={() => setSekme("yeni")}>Yeni Talep</button>
          <button onClick={() => setSekme("biletler")}>Biletler</button>
          <button onClick={() => setSekme("dashboard")}>Dashboard</button>
        </nav>
      </header>

      <main>
        {sekme === "yeni" && <NewTicketForm />}
        {sekme === "biletler" && <TicketList />}
        {sekme === "dashboard" && <Dashboard />}
      </main>
    </div>
  );
}