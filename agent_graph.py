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


graph = StateGraph(AgentState)
graph.add_node("classify", classify)
graph.set_entry_point("classify")
graph.add_edge("classify", END)
app = graph.compile()

sonuc = app.invoke({"talep": "Şifremi nasıl sıfırlarım?", "kategori": ""})
print(sonuc)