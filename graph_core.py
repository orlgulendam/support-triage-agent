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
    deneme_sayisi: int
    insan_karari: str


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
    return {"kategori": tahmin, "deneme_sayisi": 0}


def retry_classify(state: AgentState) -> AgentState:
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=50,
        messages=[{
            "role": "user",
            "content": f"Bu destek talebi daha once '{state['kategori']}' olarak "
                        f"siniflandirilmisti ama bir insan bunu reddetti, yanlis buldu. "
                        f"Talebi farkli bir acidan, daha dikkatli degerlendirip "
                        f"su 3 kategoriden birine tekrar ata: basit_soru, teknik_sorun, "
                        f"hassas_sikayet. Sadece kategori adini yaz. Talep: {state['talep']}"
        }]
    )
    tahmin = response.content[0].text.strip()
    return {"kategori": tahmin, "deneme_sayisi": state["deneme_sayisi"] + 1}


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


def awaiting_review(state: AgentState) -> AgentState:
    return {}


def finalize_human(state: AgentState) -> AgentState:
    if state["insan_karari"] == "onay":
        mesaj = f"[INSAN ONAYIYLA GONDERILDI] Kategori: {state['kategori']} (deneme: {state['deneme_sayisi']})"
        return {"cevap": mesaj}
    else:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            messages=[{
                "role": "user",
                "content": f"Bu destek talebi {state['deneme_sayisi']} kez otomatik "
                            f"siniflandirilmaya calisildi ama her seferinde reddedildi, "
                            f"su an bir insan temsilciye eskale ediliyor. Temsilciye "
                            f"yardimci olmak icin: talebin ozetini cikar, neden zor "
                            f"olabilecegini belirt, ve onerilen bir ilk yaklasim sun. "
                            f"Talep: {state['talep']}"
            }]
        )
        brifing = response.content[0].text.strip()
        mesaj = f"[ESKALE EDILDI - INSAN BRIFINGI]\n{brifing}"
        return {"cevap": mesaj}


def decide_after_classify(state: AgentState) -> str:
    if state["kategori"] == "basit_soru":
        return "draft_response"
    else:
        return "awaiting_review"


def decide_after_review(state: AgentState) -> str:
    if state["insan_karari"] == "onay":
        return "finalize_human"
    elif state["deneme_sayisi"] >= 2:
        return "finalize_human"
    else:
        return "retry_classify"


graph = StateGraph(AgentState)
graph.add_node("classify", classify)
graph.add_node("retry_classify", retry_classify)
graph.add_node("draft_response", draft_response)
graph.add_node("awaiting_review", awaiting_review)
graph.add_node("finalize_human", finalize_human)

graph.set_entry_point("classify")

graph.add_conditional_edges("classify", decide_after_classify, {
    "draft_response": "draft_response",
    "awaiting_review": "awaiting_review"
})

graph.add_conditional_edges("awaiting_review", decide_after_review, {
    "finalize_human": "finalize_human",
    "retry_classify": "retry_classify"
})

graph.add_edge("retry_classify", "awaiting_review")
graph.add_edge("draft_response", END)
graph.add_edge("finalize_human", END)

checkpointer = MemorySaver()
graph_app = graph.compile(checkpointer=checkpointer, interrupt_before=["awaiting_review"])