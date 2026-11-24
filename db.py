"""
db.py
Koneksi ke PostgreSQL cloud (Supabase atau Neon) memakai SQLAlchemy.

Tabel:
  kb_antigravity : basis pengetahuan (bisa diedit dari Table Editor Supabase/Neon)
  chat_logs      : riwayat pertanyaan & jawaban pengguna
  feedback       : penilaian 👍/👎 dari pengguna
"""

import json
import re

import pandas as pd
from sqlalchemy import create_engine, text

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS kb_antigravity (
    id          SERIAL PRIMARY KEY,
    kode        TEXT UNIQUE NOT NULL,
    topik       TEXT NOT NULL,
    judul       TEXT NOT NULL,
    konten      TEXT NOT NULL,
    kata_kunci  TEXT DEFAULT '',
    sumber      TEXT DEFAULT 'Infografis',
    updated_at  TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS chat_logs (
    id          BIGSERIAL PRIMARY KEY,
    session_id  TEXT NOT NULL,
    pertanyaan  TEXT NOT NULL,
    jawaban     TEXT NOT NULL,
    sumber      TEXT DEFAULT '[]',
    mode        TEXT,
    skor        REAL,
    created_at  TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS feedback (
    id          BIGSERIAL PRIMARY KEY,
    chat_id     BIGINT REFERENCES chat_logs(id) ON DELETE CASCADE,
    nilai       SMALLINT NOT NULL,          -- 1 = 👍, 0 = 👎
    created_at  TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_chat_logs_created ON chat_logs (created_at DESC);
"""


def buat_engine(database_url: str):
    url = str(database_url).strip()
    # Ambil hanya bagian postgresql://... (abaikan "psql '...'", tanda kutip, spasi, dll.)
    m = re.search(r"postgres(?:ql)?(?:\+\w+)?://[^\s'\"]+", url)
    if m:
        url = m.group(0)
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]
    if url.startswith("postgresql://"):
        url = "postgresql+psycopg2://" + url[len("postgresql://"):]
    connect_args = {}
    if "sslmode" not in url and "localhost" not in url and "127.0.0.1" not in url:
        connect_args["sslmode"] = "require"  # Supabase & Neon wajib SSL
    return create_engine(url, pool_pre_ping=True, pool_size=3, max_overflow=2,
                         pool_recycle=300, connect_args=connect_args)


def init_db(engine):
    with engine.begin() as conn:
        for stmt in SCHEMA_SQL.split(";"):
            if stmt.strip():
                conn.execute(text(stmt))


def seed_kb(engine, dokumen, timpa: bool = False):
    """Isi tabel kb_antigravity. timpa=False -> hanya menambah dokumen yang belum ada,
    sehingga editan manual di Supabase/Neon tidak tertimpa."""
    aksi = """DO UPDATE SET topik=EXCLUDED.topik, judul=EXCLUDED.judul, konten=EXCLUDED.konten,
              kata_kunci=EXCLUDED.kata_kunci, sumber=EXCLUDED.sumber, updated_at=now()""" \
        if timpa else "DO NOTHING"
    sql = text(f"""
        INSERT INTO kb_antigravity (kode, topik, judul, konten, kata_kunci, sumber)
        VALUES (:kode, :topik, :judul, :konten, :kata_kunci, :sumber)
        ON CONFLICT (kode) {aksi}
    """)
    with engine.begin() as conn:
        conn.execute(sql, [{**{"kata_kunci": "", "sumber": "Infografis"}, **d} for d in dokumen])


def load_kb(engine):
    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT kode, topik, judul, konten, kata_kunci, sumber FROM kb_antigravity ORDER BY kode"
        )).mappings().all()
    return [dict(r) for r in rows]


def simpan_chat(engine, session_id, pertanyaan, hasil) -> int:
    with engine.begin() as conn:
        return conn.execute(text("""
            INSERT INTO chat_logs (session_id, pertanyaan, jawaban, sumber, mode, skor)
            VALUES (:sid, :q, :a, :src, :mode, :skor) RETURNING id
        """), {"sid": session_id, "q": pertanyaan, "a": hasil["jawaban"],
               "src": json.dumps(hasil["sumber"], ensure_ascii=False),
               "mode": hasil["mode"], "skor": hasil["skor"]}).scalar_one()


def simpan_feedback(engine, chat_id: int, nilai: int):
    with engine.begin() as conn:
        conn.execute(text("INSERT INTO feedback (chat_id, nilai) VALUES (:c, :n)"),
                     {"c": chat_id, "n": nilai})


def ambil_log(engine, limit: int = 500) -> pd.DataFrame:
    with engine.connect() as conn:
        return pd.read_sql(text("""
            SELECT c.id, c.created_at, c.session_id, c.pertanyaan, c.jawaban, c.sumber,
                   c.mode, c.skor, f.nilai AS feedback
            FROM chat_logs c
            LEFT JOIN LATERAL (SELECT nilai FROM feedback WHERE chat_id = c.id
                               ORDER BY created_at DESC LIMIT 1) f ON TRUE
            ORDER BY c.created_at DESC LIMIT :n
        """), conn, params={"n": limit})


def sensor(teks: str) -> str:
    """Sembunyikan user/password di pesan error agar tidak tampil di aplikasi publik."""
    teks = re.sub(r"(postgres(?:ql)?(?:\+\w+)?://)[^@\s'\"]+@", r"\1***:***@", str(teks))
    return re.sub(r"password=\S+", "password=***", teks)
