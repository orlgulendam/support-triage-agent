import sqlite3
from datetime import datetime

DB_PATH = "karar_gunlugu.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kararlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            zaman TEXT,
            talep TEXT,
            kategori TEXT,
            deneme_sayisi INTEGER,
            insan_karari TEXT,
            sonuc_tipi TEXT,
            cevap TEXT
        )
    """)
    conn.commit()
    conn.close()


def log_karar(talep, kategori, deneme_sayisi, insan_karari, sonuc_tipi, cevap):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO kararlar (zaman, talep, kategori, deneme_sayisi, insan_karari, sonuc_tipi, cevap)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        talep,
        kategori,
        deneme_sayisi,
        insan_karari,
        sonuc_tipi,
        cevap
    ))
    conn.commit()
    conn.close()