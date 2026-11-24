"""
app.py — AntiGravBot
Chatbot materi "Google Antigravity 2.0" berbasis Streamlit + PostgreSQL (Supabase/Neon) + Gemini.

Jalankan lokal :  streamlit run app.py
Secrets (Streamlit Cloud > Settings > Secrets, atau .streamlit/secrets.toml):
    DATABASE_URL   = "postgresql://..."      # Supabase / Neon
    GEMINI_API_KEY = "AIza..."               # opsional, dari aistudio.google.com
    GEMINI_MODEL   = "gemini-flash-latest"   # opsional
    ADMIN_PASSWORD = "ganti-password"        # untuk halaman Dashboard
"""

import json
import os
import uuid
from pathlib import Path

import pandas as pd
import streamlit as st

import db
from engine import ChatbotAntigravity
from knowledge_base import CONTOH_PERTANYAAN, DATA_UJI, DOKUMEN, INFO_MATERI

NAMA_MAHASISWA = "RENXY LICHANDY"
IDENTITAS = "Mahasiswa | 261012000110"

st.set_page_config(page_title="AntiGravBot · Google Antigravity 2.0", page_icon="🚀", layout="wide")

st.markdown("""
<style>
.hero {padding:1.1rem 1.4rem;border-radius:14px;margin-bottom:1rem;
       background:linear-gradient(120deg,#0b1f3a 0%,#123f73 55%,#1b6fb3 100%);color:#fff;}
.hero h2 {margin:0;color:#fff;font-size:1.55rem}
.hero p {margin:.35rem 0 0;opacity:.85}
.author {margin-top:.7rem;padding-top:.6rem;border-top:1px solid rgba(255,255,255,.25);font-size:.9rem}
.author b {letter-spacing:.04em}
.badge {display:inline-block;padding:2px 9px;border-radius:99px;font-size:.75rem;margin-right:6px;
        background:#e8f1fb;color:#123f73;border:1px solid #c5dcf3}
</style>""", unsafe_allow_html=True)


# ---------------------------------------------------------------- konfigurasi
def rahasia(kunci, default=None):
    try:
        if kunci in st.secrets:
            return st.secrets[kunci]
    except Exception:
        pass
    return os.environ.get(kunci, default)


DATABASE_URL = rahasia("DATABASE_URL")
GEMINI_API_KEY = rahasia("GEMINI_API_KEY")
GEMINI_MODEL = rahasia("GEMINI_MODEL", "gemini-flash-latest")
ADMIN_PASSWORD = rahasia("ADMIN_PASSWORD", "admin123")


@st.cache_resource(show_spinner="Menghubungkan ke database…")
def _engine_tersambung(url):
    # Error tidak di-cache (exception dilempar), jadi koneksi dicoba ulang di run berikutnya.
    eng = db.buat_engine(url)
    db.init_db(eng)
    db.seed_kb(eng, DOKUMEN)
    return eng


def get_engine():
    if not DATABASE_URL:
        return None, "DATABASE_URL belum diisi"
    try:
        return _engine_tersambung(DATABASE_URL), None
    except Exception as e:
        return None, db.sensor(e)


@st.cache_data(ttl=600, show_spinner=False)
def muat_dokumen(url):
    eng, _ = get_engine()
    if eng is not None:
        try:
            docs = db.load_kb(eng)
            if docs:
                return json.dumps(docs), "database"
        except Exception:
            pass
    return json.dumps(DOKUMEN), "lokal"


@st.cache_resource(show_spinner=False)
def get_bot(docs_json: str, api_key, model):
    return ChatbotAntigravity(json.loads(docs_json), api_key=api_key, model=model)


ENGINE, DB_ERROR = get_engine()
DOCS_JSON, SUMBER_KB = muat_dokumen(DATABASE_URL or "")
BOT = get_bot(DOCS_JSON, GEMINI_API_KEY, GEMINI_MODEL)

if "session_id" not in st.session_state:
    st.session_state.session_id = uuid.uuid4().hex[:12]
    st.session_state.pesan = []
    st.session_state.feedback_tersimpan = set()

# ------------------------------------------------------------------- sidebar
with st.sidebar:
    st.markdown("## 🚀 AntiGravBot")
    st.markdown(f"**{NAMA_MAHASISWA}**  \n{IDENTITAS}")
    halaman = st.radio("Menu", ["💬 Chatbot", "📚 Materi", "📊 Dashboard", "ℹ️ Tentang"],
                       label_visibility="collapsed")
    st.divider()
    st.markdown("**Mode jawaban**")
    opsi_mode = ["Gemini (RAG)", "Retrieval saja"] if BOT.llm_tersedia else ["Retrieval saja"]
    mode = st.radio("Mode", opsi_mode, label_visibility="collapsed")
    if not BOT.llm_tersedia:
        st.caption("Isi `GEMINI_API_KEY` di Secrets untuk mengaktifkan mode Gemini.")
    st.divider()
    st.markdown("**Status sistem**")
    st.markdown(f"{'🟢' if ENGINE else '🔴'} Database: {'terhubung' if ENGINE else 'tidak terhubung'}")
    st.markdown(f"{'🟢' if BOT.llm_tersedia else '⚪'} Gemini: {BOT.model if BOT.llm_tersedia else 'nonaktif'}")
    if BOT.llm_tersedia and getattr(BOT, "error_terakhir", None):
        with st.expander("Detail error Gemini"):
            st.caption(db.sensor(BOT.error_terakhir)[:900])
    st.markdown(f"📄 Basis pengetahuan: {len(BOT.dokumen)} dokumen ({SUMBER_KB})")
    if DB_ERROR and DATABASE_URL:
        with st.expander("Detail error database"):
            st.code(DB_ERROR[:400])
    st.divider()
    if st.button("🧹 Mulai percakapan baru", width="stretch"):
        st.session_state.pesan = []
        st.session_state.session_id = uuid.uuid4().hex[:12]
        st.rerun()


# ------------------------------------------------------------------ halaman
def hero():
    st.markdown(f"""<div class="hero"><h2>{INFO_MATERI['judul']}</h2>
    <p>{INFO_MATERI['subjudul']}</p>
    <div class="author">Disusun oleh: <b>{NAMA_MAHASISWA}</b> · {IDENTITAS}</div></div>""", unsafe_allow_html=True)


def tampil_pesan(i, m):
    with st.chat_message(m["role"], avatar="🧑‍🎓" if m["role"] == "user" else "🤖"):
        st.markdown(m["content"])
        if m["role"] == "assistant":
            meta = f"<span class='badge'>mode: {m.get('mode', '-')}</span>"
            if m.get("skor") is not None and m.get("mode") not in ("intent",):
                meta += f"<span class='badge'>relevansi: {m['skor']:.2f}</span>"
            for s in m.get("sumber", []):
                meta += f"<span class='badge'>📄 {s}</span>"
            st.markdown(meta, unsafe_allow_html=True)
            cid = m.get("chat_id")
            if cid and ENGINE is not None:
                nilai = st.feedback("thumbs", key=f"fb_{cid}")
                if nilai is not None and cid not in st.session_state.feedback_tersimpan:
                    try:
                        db.simpan_feedback(ENGINE, cid, int(nilai))
                        st.session_state.feedback_tersimpan.add(cid)
                        st.toast("Terima kasih atas penilaiannya!")
                    except Exception as e:
                        st.toast(f"Gagal menyimpan feedback: {e}")


def proses(pertanyaan):
    st.session_state.pesan.append({"role": "user", "content": pertanyaan})
    riwayat = [{"role": m["role"], "content": m["content"]} for m in st.session_state.pesan[:-1]]
    with st.spinner("AntiGravBot sedang berpikir…"):
        hasil = BOT.jawab(pertanyaan, riwayat=riwayat, pakai_llm=(mode == "Gemini (RAG)"))
    chat_id = None
    if ENGINE is not None:
        try:
            chat_id = db.simpan_chat(ENGINE, st.session_state.session_id, pertanyaan, hasil)
        except Exception as e:
            st.toast(f"Log tidak tersimpan: {e}")
    st.session_state.pesan.append({"role": "assistant", "content": hasil["jawaban"],
                                   "mode": hasil["mode"], "skor": hasil["skor"],
                                   "sumber": hasil["sumber"], "chat_id": chat_id})


if halaman == "💬 Chatbot":
    hero()
    if not st.session_state.pesan:
        st.markdown("**Coba pertanyaan berikut:**")
        kolom = st.columns(3)
        for i, q in enumerate(CONTOH_PERTANYAAN):
            if kolom[i % 3].button(q, key=f"contoh_{i}", width="stretch"):
                st.session_state.antrian = q
                st.rerun()

    for i, m in enumerate(st.session_state.pesan):
        tampil_pesan(i, m)

    masukan = st.chat_input("Tanyakan apa saja tentang Google Antigravity 2.0…")
    if "antrian" in st.session_state:
        masukan = st.session_state.pop("antrian")
    if masukan:
        proses(masukan)
        st.rerun()

elif halaman == "📚 Materi":
    hero()
    base = Path(__file__).parent
    gambar = next((g for g in (base / "assets" / "infografis.png", base / "infografis.png") if g.exists()), None)
    if gambar:
        st.image(str(gambar), caption="Materi sumber: infografis Google Antigravity 2.0",
                 width="stretch")
    st.subheader("Basis pengetahuan chatbot")
    df = pd.DataFrame(BOT.dokumen)
    for topik, grup in df.groupby("topik", sort=False):
        st.markdown(f"#### {topik}")
        for _, d in grup.iterrows():
            with st.expander(f"{d['kode']} · {d['judul']}  —  _{d.get('sumber', '')}_"):
                st.markdown(d["konten"])

elif halaman == "📊 Dashboard":
    st.header("📊 Dashboard Admin")
    if st.text_input("Password admin", type="password") != ADMIN_PASSWORD:
        st.info("Masukkan password admin untuk melihat statistik.")
        st.stop()

    tab1, tab2 = st.tabs(["Statistik percakapan", "Evaluasi akurasi"])
    with tab1:
        if ENGINE is None:
            st.warning("Database belum terhubung, jadi log percakapan belum tersedia.")
        else:
            log = db.ambil_log(ENGINE)
            if log.empty:
                st.info("Belum ada percakapan.")
            else:
                fb = log["feedback"].dropna()
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Total pertanyaan", len(log))
                c2.metric("Sesi unik", log["session_id"].nunique())
                c3.metric("Rata-rata relevansi", f"{log['skor'].mean():.2f}")
                c4.metric("Feedback positif", f"{(fb.mean() * 100):.0f}%" if len(fb) else "–")

                log["topik"] = log["sumber"].apply(
                    lambda s: (json.loads(s) or ["(sapaan/di luar materi)"])[0])
                a, b = st.columns(2)
                a.markdown("**Topik paling sering ditanyakan**")
                a.bar_chart(log["topik"].value_counts(), horizontal=True)
                b.markdown("**Mode jawaban**")
                b.bar_chart(log["mode"].value_counts())
                st.markdown("**Percakapan terbaru**")
                st.dataframe(log[["created_at", "pertanyaan", "mode", "skor", "feedback"]].head(50),
                             width="stretch", hide_index=True)
                st.download_button("⬇️ Unduh semua log (CSV)", log.to_csv(index=False).encode(),
                                   "chat_logs_antigravbot.csv", "text/csv")
    with tab2:
        baris, a1, a3 = BOT.evaluasi(DATA_UJI)
        c1, c2, c3 = st.columns(3)
        c1.metric("Jumlah data uji", len(baris))
        c2.metric("Akurasi Top-1", f"{a1 * 100:.0f}%")
        c3.metric("Akurasi Top-3", f"{a3 * 100:.0f}%")
        st.dataframe(pd.DataFrame(baris), width="stretch", hide_index=True)

else:
    hero()
    st.subheader("Arsitektur AntiGravBot")
    st.graphviz_chart("""
    digraph G { rankdir=LR; node [shape=box, style="rounded,filled", fillcolor="#e8f1fb", fontname="Helvetica"];
      U [label="Pengguna\\n(browser)"]; S [label="Streamlit\\n(app.py)"]; R [label="Retriever\\nTF-IDF kata+karakter"];
      G [label="Google Gemini\\n(RAG, opsional)"]; D [label="PostgreSQL\\nSupabase / Neon", fillcolor="#fff3d6"];
      U -> S -> R; R -> G [label="konteks"]; G -> S [label="jawaban"]; S -> D [label="log & feedback"];
      D -> R [label="knowledge base"]; }
    """)
    st.markdown(f"""
**Cara kerja**
1. Pertanyaan pengguna dinormalisasi (huruf kecil, buang tanda baca & stopword, samakan sinonim).
2. **Retriever** mengukur kemiripan pertanyaan dengan 17 dokumen materi memakai *TF-IDF* kata
   (bobot 0,6) dan *TF-IDF* n-gram karakter (bobot 0,4) + *cosine similarity*.
3. Jika skor di bawah ambang (0,12) → chatbot menyatakan topik di luar materi.
4. Mode **Gemini (RAG)**: dokumen teratas dikirim sebagai konteks ke Gemini agar jawaban natural
   tetapi tetap berpijak pada materi. Mode **Retrieval**: isi dokumen ditampilkan langsung.
5. Setiap percakapan & 👍/👎 disimpan ke **PostgreSQL cloud** (Supabase/Neon) untuk dashboard.

**Disusun oleh:** {NAMA_MAHASISWA} — {IDENTITAS}

**Teknologi:** Python · Streamlit · scikit-learn · SQLAlchemy · PostgreSQL (Supabase/Neon) · Google Gemini API
""")
