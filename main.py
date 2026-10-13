import os
import secrets
import uuid
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from graph_core import graph_app
from logger import (
    init_db, log_karar, get_kararlar, get_istatistik,
    bekleyen_kaydet, bekleyen_sil, get_bekleyenler,
)

init_db()
app = FastAPI()

# Hangi adreslerden gelen tarayici isteklerine izin verilecegi.
# Canliya alirken FRONTEND_URL ortam degiskenine sitenin adresini yazacagiz.
izinli_adresler = os.getenv("FRONTEND_URL", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=izinli_adresler,
    allow_methods=["*"],
    allow_headers=["*"],
)


def temsilci_dogrula(x_panel_token: str = Header(default="")):
    """Temsilci panelinin kullandigi uclari PANEL_TOKEN ile korur."""
    beklenen = os.getenv("PANEL_TOKEN", "")
    if not beklenen:
        raise HTTPException(503, "PANEL_TOKEN ayarlanmamis")
    if not secrets.compare_digest(x_panel_token, beklenen):
        raise HTTPException(401, "Yetkisiz")


@app.get("/tickets", dependencies=[Depends(temsilci_dogrula)])
def talepleri_listele():
    return get_kararlar()


@app.get("/tickets/pending", dependencies=[Depends(temsilci_dogrula)])
def bekleyenleri_listele():
    return get_bekleyenler()


@app.get("/stats", dependencies=[Depends(temsilci_dogrula)])
def istatistikleri_getir():
    return get_istatistik()


@app.get("/panel/auth", dependencies=[Depends(temsilci_dogrula)])
def panel_giris_kontrol():
    return {"ok": True}


class YeniTalep(BaseModel):
    talep: str


class InsanKarari(BaseModel):
    karar: str  # "onay" veya "red"


def _sonuc_dondur(ticket_id, config, sonuc):
    durum = graph_app.get_state(config)
    if durum.next:
        bekleyen_kaydet(ticket_id, sonuc["talep"], sonuc["kategori"])
        return {"ticket_id": ticket_id, "durum": "beklemede", "kategori": sonuc["kategori"]}
    bekleyen_sil(ticket_id)
    _kaydet(sonuc)
    return {"ticket_id": ticket_id, "durum": "tamamlandi",
            "kategori": sonuc["kategori"], "cevap": sonuc["cevap"]}


@app.post("/tickets")
def yeni_talep_olustur(istek: YeniTalep):
    ticket_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": ticket_id}}

    sonuc = graph_app.invoke(
        {"talep": istek.talep, "kategori": "", "cevap": "",
         "deneme_sayisi": 0, "insan_karari": ""},
        config=config
    )
    return _sonuc_dondur(ticket_id, config, sonuc)


@app.post("/tickets/{ticket_id}/review", dependencies=[Depends(temsilci_dogrula)])
def insan_karari_bildir(ticket_id: str, istek: InsanKarari):
    config = {"configurable": {"thread_id": ticket_id}}

    if not graph_app.get_state(config).next:
        raise HTTPException(404, "Onay bekleyen talep bulunamadi")

    graph_app.update_state(config, {"insan_karari": istek.karar})
    sonuc = graph_app.invoke(None, config=config)
    return _sonuc_dondur(ticket_id, config, sonuc)


def _kaydet(sonuc):
    if sonuc["kategori"] == "basit_soru":
        sonuc_tipi = "otomatik_cevap"
    elif sonuc["insan_karari"] == "onay":
        sonuc_tipi = "insan_onayli"
    else:
        sonuc_tipi = "eskale_edildi"

    log_karar(
        talep=sonuc["talep"], kategori=sonuc["kategori"],
        deneme_sayisi=sonuc["deneme_sayisi"], insan_karari=sonuc["insan_karari"],
        sonuc_tipi=sonuc_tipi, cevap=sonuc["cevap"]
    )