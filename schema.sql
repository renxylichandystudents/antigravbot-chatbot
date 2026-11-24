-- schema.sql — jalankan di Supabase (SQL Editor) atau Neon (SQL Editor).
-- Catatan: app.py juga membuat tabel ini otomatis saat pertama kali dijalankan.

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

-- Aktifkan RLS agar tabel tidak terbuka lewat REST API publik Supabase.
-- Aplikasi tetap bisa akses karena terhubung sebagai pemilik tabel (role postgres).
ALTER TABLE kb_antigravity ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_logs      ENABLE ROW LEVEL SECURITY;
ALTER TABLE feedback       ENABLE ROW LEVEL SECURITY;

-- Contoh query untuk presentasi:
-- SELECT mode, COUNT(*) FROM chat_logs GROUP BY mode;
-- SELECT pertanyaan, skor FROM chat_logs ORDER BY created_at DESC LIMIT 10;
