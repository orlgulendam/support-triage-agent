import uuid
from fastapi import FastAPI
from pydantic import BaseModel
from graph_core import graph_app
from logger import init_db, log_karar

init_db()
app = FastAPI()


class YeniTalep(BaseModel):
    talep: str


class InsanKarari(BaseModel):
    karar: str  # "onay" veya "red"


@app.post("/tickets")
def yeni_talep_olustur(istek: YeniTalep):
    ticket_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": ticket_id}}

    sonuc = graph_app.invoke(
        {"talep": istek.talep, "kategori": "", "cevap": "",
         "deneme_sayisi": 0, "insan_karari": ""},
        config=config
    )

    durum = graph_app.get_state(config)
    if durum.next:
        return {"ticket_id": ticket_id, "durum": "beklemede", "kategori": sonuc["kategori"]}
    else:
        _kaydet(sonuc)
        return {"ticket_id": ticket_id, "durum": "tamamlandi",
                "kategori": sonuc["kategori"], "cevap": sonuc["cevap"]}


@app.post("/tickets/{ticket_id}/review")
def insan_karari_bildir(ticket_id: str, istek: InsanKarari):
    config = {"configurable": {"thread_id": ticket_id}}

    graph_app.update_state(config, {"insan_karari": istek.karar})
    sonuc = graph_app.invoke(None, config=config)

    durum = graph_app.get_state(config)
    if durum.next:
        return {"ticket_id": ticket_id, "durum": "beklemede", "kategori": sonuc["kategori"]}
    else:
        _kaydet(sonuc)
        return {"ticket_id": ticket_id, "durum": "tamamlandi",
                "kategori": sonuc["kategori"], "cevap": sonuc["cevap"]}


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