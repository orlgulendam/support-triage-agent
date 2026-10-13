import { useState } from "react";
import { createTicket } from "../api";
import type { TicketResponse } from "../types";

export default function CustomerPortal() {
  const [talep, setTalep] = useState("");
  const [sonuc, setSonuc] = useState<TicketResponse | null>(null);
  const [gonderilen, setGonderilen] = useState("");
  const [yukleniyor, setYukleniyor] = useState(false);
  const [hata, setHata] = useState<string | null>(null);

  async function gonder() {
    const metin = talep.trim();
    setYukleniyor(true);
    setHata(null);
    try {
      setSonuc(await createTicket(metin));
      setGonderilen(metin);
    } catch {
      setHata("Talebiniz şu an gönderilemedi. Lütfen daha sonra tekrar deneyin.");
    } finally {
      setYukleniyor(false);
    }
  }

  function sifirla() {
    setTalep("");
    setSonuc(null);
    setGonderilen("");
    setHata(null);
  }

  return (
    <div className="narrow stack">
      {hata && <div className="alert alert-error">{hata}</div>}

      {!sonuc && (
        <form
          className="card"
          onSubmit={(e) => {
            e.preventDefault();
            gonder();
          }}
        >
          <label className="field-label" htmlFor="talep">
            Size nasıl yardımcı olabiliriz?
          </label>
          <textarea
            id="talep"
            className="textarea"
            value={talep}
            onChange={(e) => setTalep(e.target.value)}
            placeholder="Sorununuzu veya talebinizi buraya yazın"
            rows={6}
          />
          <div className="form-footer">
            <span className="muted">{talep.length} karakter</span>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={yukleniyor || !talep.trim()}
            >
              {yukleniyor ? "Gönderiliyor…" : "Gönder"}
            </button>
          </div>
        </form>
      )}

      {sonuc && (
        <div className="card stack">
          <div>
            <div className="section-label">Talebiniz</div>
            <div className="quote">{gonderilen}</div>
          </div>

          {sonuc.durum === "tamamlandi" ? (
            <div>
              <div className="section-label">Yanıt</div>
              <div className="response-text">{sonuc.cevap}</div>
            </div>
          ) : (
            <div className="alert">
              Talebiniz alındı. Müşteri temsilcimiz inceleyip size dönüş yapacak.
            </div>
          )}

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
