import sqlite3

conn = sqlite3.connect("karar_gunlugu.db")
cursor = conn.cursor()

cursor.execute("SELECT zaman, kategori, deneme_sayisi, sonuc_tipi FROM kararlar ORDER BY id DESC")
rows = cursor.fetchall()

print(f"Toplam kayit: {len(rows)}\n")
for row in rows:
    zaman, kategori, deneme, sonuc_tipi = row
    print(f"{zaman} | Kategori: {kategori} | Deneme: {deneme} | Sonuc: {sonuc_tipi}")

print("\n--- Ozet istatistikler ---")
cursor.execute("SELECT sonuc_tipi, COUNT(*) FROM kararlar GROUP BY sonuc_tipi")
for sonuc_tipi, adet in cursor.fetchall():
    print(f"{sonuc_tipi}: {adet}")

conn.close()