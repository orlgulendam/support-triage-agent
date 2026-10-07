import { useState } from "react";
import { createTicket, reviewTicket } from "../api";
import type { TicketResponse } from "../types";

export default function NewTicketForm() {
  const [talep, setTalep] = useState("");
  const [sonuc, setSonuc] = useState<TicketResponse | null>(null);
  const [yukleniyor, setYukleniyor] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setYukleniyor(true);
    const cevap = await createTicket(talep);
    setSonuc(cevap);
    setYukleniyor(false);
  }

  async function handleKarar(karar: "onay" | "red") {
    if (!sonuc) return;
    setYukleniyor(true);
    const cevap = await reviewTicket(sonuc.ticket_id, karar);
    setSonuc(cevap);
    setYukleniyor(false);
  }

  return (
    <div className="new-ticket-form">
      <form onSubmit={handleSubmit}>
        <textarea
          value={talep}
          onChange={(e) => setTalep(e.target.value)}
          placeholder="Destek talebinizi yazin..."
          rows={4}
        />
        <button type="submit" disabled={yukleniyor || !talep}>
          Gonder
        </button>
      </form>

      {yukleniyor && <p>Isleniyor...</p>}

      {sonuc && sonuc.durum === "beklemede" && (
        <div className="review-box">
          <p>
            Model, bu talebi <strong>{sonuc.kategori}</strong> olarak
            sinifllandirdi. Onayliyor musunuz?
          </p>
          <button onClick={() => handleKarar("onay")}>Onayla</button>
          <button onClick={() => handleKarar("red")}>Reddet</button>
        </div>
      )}

      {sonuc && sonuc.durum === "tamamlandi" && (
        <div className="result-box">
          <p>
            <strong>Kategori:</strong> {sonuc.kategori}
          </p>
          <p>
            <strong>Cevap:</strong> {sonuc.cevap}
          </p>
        </div>
      )}
    </div>
  );
}