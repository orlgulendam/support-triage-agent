import os
from dotenv import load_dotenv
from anthropic import Anthropic
import pandas as pd

load_dotenv()
client = Anthropic()

df = pd.read_csv("sample_tickets.csv")

dogru_sayisi = 0

for index, row in df.iterrows():
    metin = f"{str(row['subject'])} {str(row['body'])}"

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=50,
        messages=[{
            "role": "user",
            "content": f"Bu destek talebini su 3 kategoriden birine ata: "
                        f"basit_soru, teknik_sorun, hassas_sikayet. "
                        f"Sadece kategori adini yaz, baska hicbir sey yazma. "
                        f"Talep: {metin}"
        }]
    )
    tahmin = response.content[0].text.strip()

    gercek = row['gercek_kategori']
    if tahmin == gercek:
        dogru_sayisi += 1
        sonuc = "DOGRU"
    else:
        sonuc = "YANLIS"

    print(f"[{sonuc}] Tahmin: {tahmin} | Gercek: {gercek} | Konu: {str(row['subject'])[:50]}")

dogruluk_orani = (dogru_sayisi / len(df)) * 100
print(f"\nToplam dogruluk: {dogru_sayisi}/{len(df)} = %{dogruluk_orani:.1f}")