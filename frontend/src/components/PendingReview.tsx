import { useCallback, useEffect, useState } from "react";
import { fetchPending, reviewTicket } from "../api";
import type { PendingTicket } from "../types";
import { KATEGORI, etiketBul } from "../labels";
import Badge from "./Badge";

export default function PendingReview() {
  const [liste, setListe] = useState<PendingTicket[]>([]);
  const [islemde, setIslemde] = useState<string | null>(null);
  const [hata, setHata] = useState<string | null>(null);

  const yukle = useCallback(async () => {
    try {
      setListe(await fetchPending());
      setHata(null);
    } catch {
      setHata("Sunucuya ulaşılamadı. Backend'in çalıştığından emin olun.");
    }
  }, []);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    yukle();
    const t = setInterval(yukle, 5000);
    return () => clearInterval(t);
  }, [yukle]);

  async function karar(id: string, k: "onay" | "red") {
    setIslemde(id);
    try {
      await reviewTicket(id, k);
      await yukle();
    } catch {
      setHata("İşlem başarısız oldu.");
    } finally {
      setIslemde(null);
    }
  }

  return (
    <div className="narrow stack">
      {hata && <div className="alert alert-error">{hata}</div>}
      {!hata && liste.length === 0 && (
        <div className="card muted">Onay bekleyen talep yok.</div>
      )}
      {liste.map((t) => {
        const kat = etiketBul(KATEGORI, t.kategori);
        return (
          <div key={t.ticket_id} className="card stack">
            <div className="row between">
              <span className="card-title">Onay bekliyor</span>
              <Badge ton={kat.ton}>{kat.etiket}</Badge>
            </div>
            <div className="quote">{t.talep}</div>
            <div className="row">
              <button
                className="btn btn-primary"
                disabled={islemde === t.ticket_id}
                onClick={() => karar(t.ticket_id, "onay")}
              >
                Onayla
              </button>
              <button
                className="btn btn-secondary"
                disabled={islemde === t.ticket_id}
                onClick={() => karar(t.ticket_id, "red")}
              >
                Reddet, yeniden sınıflandır
              </button>
            </div>
          </div>
        );
      })}
    </div>
  );
}
