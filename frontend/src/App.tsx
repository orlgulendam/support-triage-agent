import AgentPanel from "./AgentPanel";
import CustomerPortal from "./components/CustomerPortal";
import PanelLogin from "./components/PanelLogin";
import { tokenAl } from "./api";
import { useState } from "react";
import "./App.css";

export default function App() {
  const yol = window.location.pathname.replace(/\/+$/, "");
  const [girdi, setGirdi] = useState(() => tokenAl() !== "");

  if (yol === "/panel") {
    return girdi ? (
      <AgentPanel />
    ) : (
      <PanelLogin onGiris={() => setGirdi(true)} />
    );
  }

  return (
    <div className="content" style={{ maxWidth: 720, margin: "0 auto" }}>
      <header className="page-header">
        <h1>Destek talebi</h1>
        <p>Talebinizi iletin, size en kısa sürede dönüş yapalım.</p>
      </header>
      <CustomerPortal />
    </div>
  );
}