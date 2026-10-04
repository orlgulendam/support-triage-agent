import os
from dotenv import load_dotenv
from anthropic import Anthropic
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()
client = Anthropic()


class AgentState(TypedDict):
    talep: str
    kategori: str
    cevap: str


def classify(state: AgentState) -> AgentState:
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=50,
        messages=[{
            "role": "user",
            "content": f"Bu destek talebini su 3 kategoriden birine ata: "
                        f"basit_soru, teknik_sorun, hassas_sikayet. "
                        f"Sadece kategori adini yaz. Talep: {state['talep']}"
        }]
    )
    tahmin = response.content[0].text.strip()
    return {"kategori": tahmin}


def draft_response(state: AgentState) -> AgentState:
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[{
            "role": "user",
            "content": f"Bir musteri destek temsilcisi gibi, su talebe "
                        f"kisa, nazik bir cevap taslagi yaz: {state['talep']}"
        }]
    )
    taslak = response.content[0].text.strip()
    return {"cevap": taslak}


def route_to_human(state: AgentState) -> AgentState:
    mesaj = f"[INSAN ONAYIYLA GONDERILDI] Kategori: {state['kategori']}"
    return {"cevap": mesaj}


def decide_next(state: AgentState) -> str:
    if state["kategori"] == "basit_soru":
        return "draft_response"
    else:
        return "route_to_human"


graph = StateGraph(AgentState)
graph.add_node("classify", classify)
graph.add_node("draft_response", draft_response)
graph.add_node("route_to_human", route_to_human)

graph.set_entry_point("classify")

graph.add_conditional_edges(
    "classify",
    decide_next,
    {
        "draft_response": "draft_response",
        "route_to_human": "route_to_human"
    }
)

graph.add_edge("draft_response", END)
graph.add_edge("route_to_human", END)

# --- Yeni kisim: checkpointer ve interrupt ---
checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer, interrupt_before=["route_to_human"])

# Her ayri "konusma/talep" icin benzersiz bir kimlik lazim (thread_id)
config = {"configurable": {"thread_id": "talep-1"}}

# 1. ADIM: Graph'i baslat
sonuc = app.invoke(
    {"talep": "Sistemde guvenlik acigi tespit ettim, acil yardim lazim", "kategori": "", "cevap": ""},
    config=config
)
print("Graph durdu, su an state:")
print(sonuc)
print()

# 2. ADIM: Insan burada devreye giriyor (biz, konsoldan)
print(f"--- INSAN KARARI BEKLENIYOR ---")
print(f"Kategori: {sonuc['kategori']}")
print(f"Talep: Sistemde guvenlik acigi tespit ettim, acil yardim lazim")
onay = input("Bu talebi insana yonlendirmeyi onayliyor musun? (e/h): ")

if onay.lower() == "e":
    # 3. ADIM: Graph'a "devam et" sinyali veriyoruz (None = state'i degistirme, kaldigin yerden devam et)
    son_hal = app.invoke(None, config=config)
    print()
    print("Graph tamamlandi, son hal:")
    print(son_hal)
else:
    print("Islem iptal edildi.")