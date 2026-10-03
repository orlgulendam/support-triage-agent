import pandas as pd

df = pd.read_csv("raw_tickets.csv")
print(df.columns.tolist())
print(df.head())
# --- aşağısı yeni eklenen kısım ---

# 1. Sadece İngilizce biletleri filtrele
df_en = df[df["language"] == "en"]

# 2. Kaç tane İngilizce bilet olduğunu gör (merak için)
print(f"İngilizce bilet sayısı: {len(df_en)}")

# 3. Rastgele 20 satır örnekle (random_state=42 ile her çalıştırmada aynı 20 satır gelir)
sample = df_en.sample(n=20, random_state=42)

# 4. Sadece subject ve body sütunlarını al
sample = sample[["subject", "body"]]

# 5. Boş bir "gercek_kategori" sütunu ekle (az sonra elle dolduracağız)
sample["gercek_kategori"] = ""

# 6. CSV olarak kaydet
sample.to_csv("sample_tickets.csv", index=False)
print("sample_tickets.csv olusturuldu")