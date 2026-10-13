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
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bekleyenler (
            ticket_id TEXT PRIMARY KEY,
            talep TEXT,
            kategori TEXT
        )
    """)
    conn.commit()
    conn.close()


def bekleyen_kaydet(ticket_id, talep, kategori):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT OR REPLACE INTO bekleyenler (ticket_id, talep, kategori) VALUES (?, ?, ?)",
        (ticket_id, talep, kategori),
    )
    conn.commit()
    conn.close()


def bekleyen_sil(ticket_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM bekleyenler WHERE ticket_id = ?", (ticket_id,))
    conn.commit()
    conn.close()


def get_bekleyenler():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT ticket_id, talep, kategori FROM bekleyenler"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


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


def get_kararlar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT id, zaman, talep, kategori, sonuc_tipi, cevap
        FROM kararlar
        ORDER BY id DESC
    """).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_istatistik():
    conn = sqlite3.connect(DB_PATH)
    toplam = conn.execute("SELECT COUNT(*) FROM kararlar").fetchone()[0]
    rows = conn.execute("""
        SELECT sonuc_tipi, COUNT(*)
        FROM kararlar
        GROUP BY sonuc_tipi
    """).fetchall()
    conn.close()
    return {
        "toplam": toplam,
        "dagilim": [{"tip": tip, "adet": adet} for tip, adet in rows],
    }