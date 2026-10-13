import { useState } from "react";
import { panelGirisKontrol, tokenKaydet, tokenSil } from "../api";

export default function PanelLogin({ onGiris }: { onGiris: () => void }) {
  const [token, setToken] = useState("");
  const [hata, setHata] = useState<string | null>(null);
  const [yukleniyor, setYukleniyor] = useState(false);

  async function giris() {
    setYukleniyor(true);
    setHata(null);
    tokenKaydet(token.trim());
    if (await panelGirisKontrol()) {
      onGiris();
    } else {
      tokenSil();
      setHata("Giriş anahtarı hatalı veya sunucuya ulaşılamadı.");
    }
    setYukleniyor(false);
  }

  return (
    <div className="content" style={{ maxWidth: 420, margin: "80px auto" }}>
      <header className="page-header">
        <h1>Temsilci girişi</h1>
        <p>Devam etmek için panel anahtarını girin.</p>
      </header>
      {hata && <div className="alert alert-error">{hata}</div>}
      <form
        className="card"
        onSubmit={(e) => {
          e.preventDefault();
          giris();
        }}
      >
        <label className="field-label" htmlFor="token">
          Panel anahtarı
        </label>
        <input
          id="token"
          type="password"
          className="textarea"
          value={token}
          onChange={(e) => setToken(e.target.value)}
        />
        <div className="form-footer">
          <span />
          <button
            type="submit"
            className="btn btn-primary"
            disabled={yukleniyor || !token.trim()}
          >
            {yukleniyor ? "Kontrol ediliyor…" : "Giriş yap"}
          </button>
        </div>
      </form>
    </div>
  );
}
