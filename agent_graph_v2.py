import os
from dotenv import load_dotenv
from anthropic import Anthropic
from typing import TypedDict
from langgraph.graph import StateGraph, END

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
    mesaj = f"Bu talep '{state['kategori']}' kategorisinde, bir insan temsilciye yonlendirildi."
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

app = graph.compile()

# Test 1: basit bir soru
sonuc1 = app.invoke({"talep": "Şifremi nasıl sıfırlarım?", "kategori": "", "cevap": ""})
print("TEST 1 (basit soru bekleniyor):")
print(sonuc1)
print()

# Test 2: teknik bir sorun
sonuc2 = app.invoke({"talep": "API'ye istek atınca 500 hatası alıyorum", "kategori": "", "cevap": ""})
print("TEST 2 (teknik sorun bekleniyor):")
print(sonuc2)