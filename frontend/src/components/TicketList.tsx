import { useState, useEffect } from "react";
import { fetchTickets } from "../api";
import type { Ticket } from "../types";
import TicketDetail from "./TicketDetail";

const RENK: Record<string, string> = {
  otomatik_cevap: "yesil",
  insan_onayli: "sari",
  eskale_edildi: "kirmizi",
};

export default function TicketList() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [secili, setSecili] = useState<Ticket | null>(null);

  useEffect(() => {
    fetchTickets().then((data) => setTickets(data));
  }, []);

  return (
    <div className="ticket-list-page">
      <div className="ticket-list">
        {tickets.map((t) => (
          <div
            key={t.id}
            className={`ticket-item ${RENK[t.sonuc_tipi] || ""}`}
            onClick={() => setSecili(t)}
          >
            <strong>{t.kategori}</strong>
            <p>{t.talep.slice(0, 50)}...</p>
          </div>
        ))}
      </div>
      <div className="ticket-detail-panel">
        {secili ? <TicketDetail ticket={secili} /> : <p>Bir bilet secin</p>}
      </div>
    </div>
  );
}