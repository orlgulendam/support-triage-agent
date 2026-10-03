# 1. Importlar:
import os
from dotenv import load_dotenv
from anthropic import Anthropic

# 2. .env dosyasını yükle
load_dotenv()

# 3. Client oluştur (otomatik olarak ANTHROPIC_API_KEY'i okur)
client = Anthropic()

# 4. Test edilecek 3 örnek talep
talepler = [
    "Şifremi nasıl sıfırlarım?",
    "Ürün elime kırık geldi, çok sinirliyim, iade istiyorum!",
    "API'ye istek atınca 500 hatası alıyorum, log'u ekte"
]

# 5. Her biri için modele sor ve cevabı yazdır
for talep in talepler:
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=50,
        messages=[{
            "role": "user",
            "content": f"Bu destek talebini şu 3 kategoriden birine ata: "
                        f"basit_soru, teknik_sorun, hassas_sikayet. "
                        f"Sadece kategori adını yaz, başka hiçbir şey yazma. "
                        f"Talep: {talep}"
        }]
    )
    print(f"Talep: {talep}")
    print(f"Kategori: {response.content[0].text}")
    print("---")