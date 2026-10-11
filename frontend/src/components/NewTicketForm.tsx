import { useState } from "react";
import { createTicket, reviewTicket } from "../api";
import type { TicketResponse } from "../types";
import { KATEGORI, etiketBul } from "../labels";
import Badge from "./Badge";

export default function NewTicketForm() {
  const [talep, setTalep] = useState("");
  const [sonuc, setSonuc] = useState<TicketResponse | null>(null);
  const [yukleniyor, setYukleniyor] = useState(false);
  const [hata, setHata] = useState<string | null>(null);

  async function calistir(islem: () => Promise<TicketResponse>) {
    setYukleniyor(true);
    setHata(null);
    try {
      setSonuc(await islem());
    } catch {
      setHata("Sunucuya ulaşılamadı. Backend'in çalıştığından emin olun.");
    } finally {
      setYukleniyor(false);
    }
  }

  function sifirla() {
    setTalep("");
    setSonuc(null);
    setHata(null);
  }

  const kategori = sonuc ? etiketBul(KATEGORI, sonuc.kategori) : null;

  return (
    <div className="narrow stack">
      {hata && <div className="alert alert-error">{hata}</div>}

      {!sonuc && (
        <form
          className="card"
          onSubmit={(e) => {
            e.preventDefault();
            calistir(() => createTicket(talep.trim()));
          }}
        >
          <label className="field-label" htmlFor="talep">
            Talep metni
          </label>
          <textarea
            id="talep"
            className="textarea"
            value={talep}
            onChange={(e) => setTalep(e.target.value)}
            placeholder="Müşterinin yazdığı talebi buraya yapıştırın"
            rows={6}
          />
          <div className="form-footer">
            <span className="muted">{talep.length} karakter</span>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={yukleniyor || !talep.trim()}
            >
              {yukleniyor ? "Sınıflandırılıyor…" : "Sınıflandır"}
            </button>
          </div>
        </form>
      )}

      {sonuc?.durum === "beklemede" && kategori && (
        <div className="card stack">
          <div className="row between">
            <span className="card-title">Onay bekliyor</span>
            <Badge ton="warning">İnsan kontrolü</Badge>
          </div>

          <div>
            <div className="section-label">Talep</div>
            <div className="quote">{talep}</div>
          </div>

          <p>
            Sistem bu talebi <Badge ton={kategori.ton}>{kategori.etiket}</Badge>{" "}
            olarak sınıflandırdı. Sınıflandırma doğru mu?
          </p>

          <div className="row">
            <button
              className="btn btn-primary"
              disabled={yukleniyor}
              onClick={() => calistir(() => reviewTicket(sonuc.ticket_id, "onay"))}
            >
              Onayla
            </button>
            <button
              className="btn btn-secondary"
              disabled={yukleniyor}
              onClick={() => calistir(() => reviewTicket(sonuc.ticket_id, "red"))}
            >
              Reddet, yeniden sınıflandır
            </button>
          </div>
        </div>
      )}

      {sonuc?.durum === "tamamlandi" && kategori && (
        <div className="card stack">
          <div className="row between">
            <span className="card-title">Sonuçlandı</span>
            <Badge ton={kategori.ton}>{kategori.etiket}</Badge>
          </div>

          <div>
            <div className="section-label">Talep</div>
            <div className="quote">{talep}</div>
          </div>

          <div>
            <div className="section-label">Yanıt</div>
            <div className="response-text">{sonuc.cevap}</div>
          </div>

          <div>
            <button className="btn btn-secondary" onClick={sifirla}>
              Yeni talep
            </button>
          </div>
        </div>
      )}
    </div>
  );
}