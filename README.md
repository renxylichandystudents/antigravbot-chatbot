# 🚀 AntiGravBot — Chatbot Materi Google Antigravity 2.0

Chatbot tugas kuliah untuk menjawab pertanyaan seputar materi
**"Google Antigravity 2.0: Era Baru Rekayasa Perangkat Lunak Berbasis Agen AI"**.

**Teknologi:** Python · Streamlit · scikit-learn (TF-IDF) · Google Gemini (RAG, opsional) · PostgreSQL cloud (Supabase atau Neon)

## Struktur file

| File | Fungsi |
|---|---|
| `app.py` | Aplikasi web Streamlit (Chatbot, Materi, Dashboard, Tentang) |
| `engine.py` | Mesin chatbot: retrieval TF-IDF + Gemini RAG + evaluasi |
| `knowledge_base.py` | 17 dokumen materi, contoh pertanyaan, 20 data uji |
| `db.py` | Koneksi & query PostgreSQL (Supabase/Neon) |
| `schema.sql` | Skrip pembuatan tabel (opsional, karena app membuat tabel otomatis) |
| `AntiGravBot_Colab.ipynb` | Notebook Google Colab (demo, evaluasi, isi database) |
| `.streamlit/secrets.toml.example` | Contoh pengisian secrets |

---

## Langkah 1 — Siapkan database (pilih salah satu)

### Opsi A: Supabase
1. Buka https://supabase.com → **New project** (region: Southeast Asia/Singapore). Catat password database.
2. Buka **SQL Editor** → tempel isi `schema.sql` → **Run**.
3. Klik tombol **Connect** di atas → tab **Connection string** → pilih **Session pooler**.
   Salin URL-nya, ganti `[YOUR-PASSWORD]` dengan password Anda.
   > Pakai *Session pooler* (host `...pooler.supabase.com`), **bukan** *Direct connection*:
   > koneksi langsung Supabase hanya IPv6 sehingga sering gagal dari Streamlit Cloud/Colab.

### Opsi B: Neon
1. Buka https://neon.tech → **Create project** (region: Asia Pacific/Singapore).
2. **SQL Editor** → tempel isi `schema.sql` → **Run**.
3. **Dashboard → Connect** → centang **Connection pooling** → salin connection string
   (sudah berisi `?sslmode=require`).

## Langkah 2 — (Opsional) API key Gemini
Buat API key gratis di https://aistudio.google.com/apikey. Tanpa API key, chatbot tetap
berjalan dalam mode **Retrieval**.

## Langkah 3 — Uji di Google Colab
1. Buka https://colab.research.google.com → **File → Upload notebook** → pilih `AntiGravBot_Colab.ipynb`.
2. Klik ikon 🔑 **Secrets** di panel kiri, tambahkan `DATABASE_URL` (dan `GEMINI_API_KEY` bila ada),
   aktifkan *Notebook access*.
3. **Runtime → Run all**. Notebook akan mengevaluasi akurasi, mengisi tabel di database, dan
   menyediakan chat interaktif.

## Langkah 4 — Publikasikan di Streamlit Community Cloud (akses publik)
1. Buat repository baru di GitHub, upload semua file di folder ini
   (**jangan** upload `secrets.toml` berisi password).
2. Buka https://share.streamlit.io → **Create app** → pilih repo, branch `main`, file `app.py`.
3. **Advanced settings → Secrets**, tempel:
   ```toml
   DATABASE_URL = "postgresql://...connection string Anda..."
   GEMINI_API_KEY = "AIza..."
   GEMINI_MODEL = "gemini-2.5-flash"
   ADMIN_PASSWORD = "password-dashboard-anda"
   ```
4. **Deploy** → Anda mendapat URL publik `https://nama-app.streamlit.app` untuk dibagikan ke
   dosen dan teman kelas.

Menjalankan di komputer sendiri:
```bash
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # lalu isi
streamlit run app.py
```

---

## Cara kerja (untuk presentasi)
1. **Pra-pemrosesan**: huruf kecil, hapus tanda baca & stopword Bahasa Indonesia, samakan sinonim
   (mis. *moda→mode*, *artefak→artifacts*, *vscode→vs code*).
2. **Retrieval**: kemiripan *cosine* antara pertanyaan dan 17 dokumen materi dengan gabungan
   TF-IDF kata (bobot 0,6) dan TF-IDF n-gram karakter 3–5 (bobot 0,4) agar tahan salah ketik.
3. **Ambang relevansi 0,12**: di bawahnya, chatbot menyatakan topik di luar materi dan memberi saran.
4. **Gemini RAG** (opsional): dokumen teratas dijadikan konteks untuk Gemini; jika gagal, otomatis
   kembali ke mode Retrieval.
5. **Database**: knowledge base, log percakapan, dan feedback 👍/👎 tersimpan di PostgreSQL cloud dan
   ditampilkan di halaman **Dashboard** (password admin).

**Hasil evaluasi retrieval** (20 pertanyaan uji): Top-1 **95%**, Top-3 **100%**.
Pertanyaan di luar materi (mis. "resep rendang", "apa itu kubernetes") ditolak dengan benar.

> Knowledge base dapat diedit langsung di Table Editor Supabase/Neon (tabel `kb_antigravity`);
> perubahan terbaca aplikasi maksimal 10 menit kemudian.
