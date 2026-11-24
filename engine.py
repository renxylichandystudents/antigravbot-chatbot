"""
engine.py
Mesin chatbot AntiGravBot.

Dua mode jawaban:
  1. RETRIEVAL  : mencari dokumen paling relevan dengan TF-IDF (kata + karakter)
                  lalu menampilkan isinya. Tidak butuh API key, selalu jalan.
  2. GEMINI-RAG : dokumen hasil retrieval dikirim sebagai konteks ke Google Gemini
                  (Retrieval-Augmented Generation) agar jawaban lebih natural.
                  Jika API key kosong / error, otomatis kembali ke mode RETRIEVAL.
"""

import re

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------------------------------------------------------
# Pra-pemrosesan teks Bahasa Indonesia
# ---------------------------------------------------------------------------
STOPWORDS = {
    "yang", "dan", "di", "ke", "dari", "apa", "itu", "ini", "adalah", "untuk", "dengan",
    "pada", "dalam", "saya", "aku", "kamu", "anda", "apakah", "bagaimana", "gimana",
    "jelaskan", "tolong", "sebutkan", "mengenai", "tentang", "sih", "dong", "ya", "kah",
    "nya", "atau", "juga", "bisa", "ada", "saja", "the", "a", "of", "is", "what",
    "mohon", "coba", "berikan", "boleh", "kan", "lah", "pun", "akan", "sebagai",
}

SINONIM = {
    "agent": "agen", "agents": "agen", "artefak": "artifacts", "artifact": "artifacts",
    "moda": "mode", "dasbor": "dashboard", "dasboard": "dashboard", "vscode": "vs code",
    "jet": "jetbrains", "intellij": "jetbrains", "screenshot": "tangkapan layar",
    "beda": "perbedaan", "bedanya": "perbedaan", "membedakan": "perbedaan",
    "kelebihan": "manfaat", "kelebihannya": "manfaat", "keunggulan": "manfaat",
    "risiko": "risiko tantangan", "risikonya": "risiko tantangan",
    "workflow": "alur kerja", "otomatis": "auto", "terminal": "cli",
}


def normalisasi(teks: str) -> str:
    teks = teks.lower()
    teks = teks.replace("agents.md", "agents md").replace("skills.md", "skills md")
    teks = re.sub(r"[^a-z0-9\s]", " ", teks)
    token = []
    for t in teks.split():
        t = SINONIM.get(t, t)
        token.extend(x for x in t.split() if x not in STOPWORDS)
    return " ".join(token)


# ---------------------------------------------------------------------------
# Jawaban untuk sapaan / percakapan ringan (intent sederhana)
# ---------------------------------------------------------------------------
INTENT = [
    (r"^(hai|halo|hallo|hi|hello|hey|selamat (pagi|siang|sore|malam)|assalamualaikum)\b",
     "Halo! 👋 Saya **AntiGravBot**, asisten belajar materi *Google Antigravity 2.0*. "
     "Silakan tanya tentang 4 pilar platform, Editor View vs Manager View, "
     "Artifacts, atau tingkat otonomi Off/Auto/Turbo."),
    (r"(terima ?kasih|makasih|thanks|thank you|thx)",
     "Sama-sama! Senang bisa membantu. Ada lagi yang ingin ditanyakan tentang Antigravity 2.0? 🚀"),
    (r"(siapa (kamu|anda)|kamu siapa|nama kamu)",
     "Saya **AntiGravBot**, chatbot yang dibangun untuk menjawab pertanyaan seputar materi "
     "*Google Antigravity 2.0: Era Baru Rekayasa Perangkat Lunak Berbasis Agen AI*."),
    (r"^(bantuan|help|menu|bisa apa|kamu bisa apa)",
     "Saya bisa menjelaskan:\n- Gambaran umum Antigravity 2.0\n- 4 pilar utama "
     "(Desktop Agent Manager, IDE & Ext, CLI & SDK, Agents & Skills)\n- Verifikasi via Artifacts\n"
     "- Editor View vs Manager View\n- 3 tingkat otonomi (Off, Auto, Turbo)\n- Alur kerja, manfaat, dan tips aman"),
]

SYSTEM_PROMPT = (
    "Kamu adalah AntiGravBot, asisten pembelajaran untuk materi kuliah "
    "'Google Antigravity 2.0: Era Baru Rekayasa Perangkat Lunak Berbasis Agen AI'. "
    "Jawab dalam Bahasa Indonesia yang jelas, ramah, dan ringkas (maksimal ±150 kata), "
    "boleh memakai poin atau tabel markdown. Jawab HANYA berdasarkan KONTEKS MATERI yang diberikan. "
    "Jangan mengarang fitur, angka, atau fakta yang tidak ada di konteks. Jika pertanyaan berada di "
    "luar materi, katakan dengan sopan bahwa materi tidak membahasnya, lalu sarankan topik yang tersedia."
)


class ChatbotAntigravity:
    def __init__(self, dokumen, api_key=None, model="gemini-flash-latest", ambang=0.12):
        self.dokumen = list(dokumen)
        self.ambang = ambang
        self.model = model
        self.api_key = api_key
        self._client = None

        korpus = [
            f"{d['judul']} {d['judul']} {d.get('kata_kunci', '')} {d['konten']}"
            for d in self.dokumen
        ]
        self.vec_kata = TfidfVectorizer(preprocessor=normalisasi, ngram_range=(1, 2), sublinear_tf=True)
        self.vec_huruf = TfidfVectorizer(preprocessor=normalisasi, analyzer="char_wb",
                                         ngram_range=(3, 5), sublinear_tf=True)
        self.mat_kata = self.vec_kata.fit_transform(korpus)
        self.mat_huruf = self.vec_huruf.fit_transform(korpus)

    # ------------------------------------------------------------------ LLM
    @property
    def llm_tersedia(self) -> bool:
        return bool(self.api_key)

    def _gemini(self):
        if self._client is None:
            from google import genai  # pip install google-genai
            self._client = genai.Client(api_key=self.api_key)
        return self._client

    # ------------------------------------------------------------ retrieval
    def cari(self, pertanyaan: str, k: int = 3):
        q_kata = self.vec_kata.transform([pertanyaan])
        q_huruf = self.vec_huruf.transform([pertanyaan])
        skor = 0.6 * cosine_similarity(q_kata, self.mat_kata)[0] + \
               0.4 * cosine_similarity(q_huruf, self.mat_huruf)[0]
        urut = np.argsort(skor)[::-1][:k]
        return [(self.dokumen[i], float(skor[i])) for i in urut]

    # --------------------------------------------------------------- jawab
    def jawab(self, pertanyaan: str, riwayat=None, pakai_llm: bool = True) -> dict:
        teks = pertanyaan.strip()
        for pola, balasan in INTENT:
            if re.search(pola, teks.lower()):
                return {"jawaban": balasan, "sumber": [], "mode": "intent", "skor": 1.0}

        hasil = self.cari(teks, k=4)
        top_doc, top_skor = hasil[0]

        if top_skor < self.ambang:
            saran = ", ".join(f"*{d['judul']}*" for d, _ in hasil[:3])
            return {
                "jawaban": "Maaf, sepertinya pertanyaan itu belum dibahas dalam materi Antigravity 2.0. "
                           f"Mungkin maksud Anda salah satu topik ini: {saran}?",
                "sumber": [], "mode": "fallback", "skor": top_skor,
            }

        relevan = [(d, s) for d, s in hasil if s >= max(self.ambang, 0.5 * top_skor)]

        if pakai_llm and self.llm_tersedia:
            try:
                jawaban = self._jawab_llm(teks, relevan, riwayat or [])
                return {"jawaban": jawaban, "sumber": [d["judul"] for d, _ in relevan],
                        "mode": "gemini-rag", "skor": top_skor}
            except Exception as e:  # jaringan/kuota/API key salah -> fallback
                self.error_terakhir = str(e)

        jawaban = f"**{top_doc['judul']}**\n\n{top_doc['konten']}"
        lain = [d["judul"] for d, s in relevan[1:3] if d["kode"] != top_doc["kode"]]
        if lain:
            jawaban += "\n\n🔎 *Topik terkait:* " + " · ".join(lain)
        return {"jawaban": jawaban, "sumber": [top_doc["judul"]], "mode": "retrieval", "skor": top_skor}

    def _jawab_llm(self, pertanyaan, relevan, riwayat):
        from google.genai import types

        konteks = "\n\n".join(f"[{d['kode']}] {d['judul']}\n{d['konten']}" for d, _ in relevan)
        histori = "\n".join(f"{m['role'].upper()}: {m['content']}" for m in riwayat[-6:])
        prompt = (
            f"KONTEKS MATERI:\n{konteks}\n\n"
            f"RIWAYAT PERCAKAPAN:\n{histori or '-'}\n\n"
            f"PERTANYAAN MAHASISWA: {pertanyaan}"
        )
        # Coba model yang diatur, lalu alias "latest" dari Google bila model lama sudah dihentikan.
        kandidat = list(dict.fromkeys([self.model, "gemini-flash-latest", "gemini-flash-lite-latest"]))
        error = None
        for nama in kandidat:
            try:
                resp = self._gemini().models.generate_content(
                    model=nama,
                    contents=prompt,
                    config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, temperature=0.3),
                )
                if resp.text:
                    self.model = nama          # ingat model yang berhasil
                    return resp.text.strip()
                error = RuntimeError("Respons Gemini kosong")
            except Exception as e:
                error = e
                pesan = str(e).lower()
                # Hanya pindah model jika model tidak ditemukan / tidak diizinkan; error lain langsung dilempar
                if not any(k in pesan for k in ("not found", "404", "not supported", "permission", "403")):
                    raise
        raise error

    # ------------------------------------------------------------ evaluasi
    def evaluasi(self, data_uji):
        """Hitung akurasi top-1 dan top-3 retrieval terhadap data uji."""
        baris, benar1, benar3 = [], 0, 0
        for q, kode in data_uji:
            hasil = self.cari(q, k=3)
            prediksi = [d["kode"] for d, _ in hasil]
            b1, b3 = prediksi[0] == kode, kode in prediksi
            benar1 += b1
            benar3 += b3
            baris.append({"pertanyaan": q, "target": kode, "prediksi": prediksi[0],
                          "skor": round(hasil[0][1], 3), "top1_benar": b1, "top3_benar": b3})
        n = len(data_uji)
        return baris, benar1 / n, benar3 / n
