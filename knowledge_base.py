"""
knowledge_base.py
Basis pengetahuan chatbot, disusun dari materi infografis
"Google Antigravity 2.0: Era Baru Rekayasa Perangkat Lunak Berbasis Agen AI".

Setiap dokumen punya:
  kode       : ID unik (dipakai sebagai primary key di database)
  topik      : kelompok materi
  judul      : judul singkat
  konten     : isi jawaban
  kata_kunci : sinonim/kata kunci tambahan agar pencarian lebih akurat
  sumber     : "Infografis" (langsung dari materi) atau
               "Penjelasan tambahan" (uraian pendukung dari isi infografis)
"""

INFO_MATERI = {
    "judul": "Google Antigravity 2.0: Era Baru Rekayasa Perangkat Lunak Berbasis Agen AI",
    "subjudul": (
        "Paradigma baru: platform semi-otonom untuk eksekusi perangkat lunak "
        "end-to-end dari perancangan hingga pengujian."
    ),
}

DOKUMEN = [
    {
        "kode": "AG-00",
        "topik": "Gambaran Umum",
        "judul": "Apa itu Google Antigravity 2.0",
        "kata_kunci": "google antigravity 2 0 antigravity antigravity pengertian definisi apa itu antigravity platform agen ai paradigma baru "
                      "semi otonom end to end rekayasa perangkat lunak software engineering",
        "konten": (
            "Google Antigravity 2.0 adalah platform rekayasa perangkat lunak berbasis agen AI "
            "yang disebut sebagai era baru pengembangan software. Paradigmanya adalah platform "
            "semi-otonom untuk mengeksekusi pengembangan perangkat lunak secara end-to-end, "
            "mulai dari perancangan hingga pengujian. Pengembang tidak lagi hanya menulis kode "
            "baris demi baris, tetapi mendelegasikan pekerjaan kepada agen AI, memantau kerjanya, "
            "lalu memverifikasi hasilnya."
        ),
        "sumber": "Infografis",
    },
    {
        "kode": "AG-01",
        "topik": "4 Pilar Utama",
        "judul": "4 Pilar Utama Platform Antigravity 2.0",
        "kata_kunci": "empat pilar utama komponen fitur utama bagian platform struktur arsitektur",
        "konten": (
            "Infografis menyebut 4 pilar utama platform Antigravity 2.0:\n"
            "1. **Desktop Agent Manager** – aplikasi mandiri untuk mengorkestrasi dan memantau "
            "beberapa agen AI secara paralel di berbagai proyek.\n"
            "2. **Antigravity IDE & Ext** – lingkungan pengembangan berbasis AI serta ekstensi "
            "integrasi untuk VS Code, JetBrains, dan Zed.\n"
            "3. **CLI dan SDK Fleksibel** – antarmuka baris perintah dan kit pengembang untuk "
            "otomatisasi skrip kustom di sisi server.\n"
            "4. **Konfigurasi Agents & Skills** – definisi peran tim melalui berkas agents.md dan "
            "panduan instruksi modular dalam skills.md.\n\n"
            "Selain itu, hasil kerja agen diperiksa lewat **Verifikasi via Artifacts**."
        ),
        "sumber": "Infografis",
    },
    {
        "kode": "AG-02",
        "topik": "4 Pilar Utama",
        "judul": "Desktop Agent Manager",
        "kata_kunci": "desktop agent manager aplikasi mandiri orkestrasi orkestrator memantau "
                      "monitoring banyak agen paralel multi proyek",
        "konten": (
            "Desktop Agent Manager adalah aplikasi mandiri (standalone) untuk mengorkestrasi dan "
            "memantau beberapa agen AI secara paralel di berbagai proyek. Dengan pilar ini, satu "
            "pengembang dapat menjalankan beberapa agen sekaligus, misalnya satu agen membuat "
            "fitur, satu menulis pengujian, dan satu memperbaiki bug, lalu memantau semuanya dari "
            "satu tempat."
        ),
        "sumber": "Infografis",
    },
    {
        "kode": "AG-03",
        "topik": "4 Pilar Utama",
        "judul": "Antigravity IDE & Extension",
        "kata_kunci": "ide extension ekstensi plugin vs code vscode jetbrains intellij zed editor "
                      "lingkungan pengembangan integrasi",
        "konten": (
            "Antigravity IDE & Ext adalah lingkungan pengembangan (IDE) berbasis AI, ditambah "
            "ekstensi integrasi untuk editor populer: **VS Code, JetBrains, dan Zed**. Jadi "
            "pengembang bisa memakai kemampuan agen Antigravity tanpa harus meninggalkan editor "
            "yang sudah biasa dipakai."
        ),
        "sumber": "Infografis",
    },
    {
        "kode": "AG-04",
        "topik": "4 Pilar Utama",
        "judul": "CLI dan SDK Fleksibel",
        "kata_kunci": "cli command line terminal baris perintah sdk software development kit "
                      "otomatisasi skrip kustom server side backend pipeline ci cd",
        "konten": (
            "CLI dan SDK Fleksibel terdiri dari antarmuka baris perintah (CLI) dan kit pengembang "
            "(SDK) untuk otomatisasi skrip kustom di sisi server (server-side). Pilar ini membuat "
            "agen bisa dipanggil dari terminal atau disisipkan ke dalam skrip dan alur otomatisasi "
            "sendiri, tidak hanya lewat tampilan grafis."
        ),
        "sumber": "Infografis",
    },
    {
        "kode": "AG-05",
        "topik": "4 Pilar Utama",
        "judul": "Konfigurasi Agents & Skills",
        "kata_kunci": "konfigurasi agents md skills md agents.md skills.md peran tim role "
                      "instruksi modular berkas file markdown pengaturan agen",
        "konten": (
            "Konfigurasi Agents & Skills adalah cara mendefinisikan perilaku agen:\n"
            "- **agents.md** – berkas untuk mendefinisikan peran tim (misalnya agen frontend, "
            "agen backend, agen penguji).\n"
            "- **skills.md** – panduan instruksi yang bersifat modular, sehingga satu keahlian "
            "dapat dipakai ulang oleh agen yang berbeda.\n\n"
            "Karena berbentuk berkas teks, konfigurasi ini mudah dibagikan dan disimpan bersama "
            "kode proyek."
        ),
        "sumber": "Infografis",
    },
    {
        "kode": "AG-06",
        "topik": "Verifikasi",
        "judul": "Verifikasi via Artifacts",
        "kata_kunci": "verifikasi artifacts artifacts artifacts artefak bukti hasil kerja transparan dokumen rencana "
                      "tangkapan layar screenshot rekaman pengujian visual video review",
        "konten": (
            "Verifikasi via Artifacts berarti hasil kerja agen disajikan secara transparan melalui "
            "**dokumen rencana, tangkapan layar, dan rekaman pengujian visual**. Pengembang tidak "
            "perlu membaca setiap baris kode yang ditulis agen; cukup memeriksa artefak tersebut "
            "untuk menilai apakah rencana dan hasilnya sudah benar sebelum diterima."
        ),
        "sumber": "Infografis",
    },
    {
        "kode": "AG-07",
        "topik": "Mode Tampilan",
        "judul": "Editor View",
        "kata_kunci": "editor view tampilan editor ide tradisional vs code manual menulis kode "
                      "baris kode perbaikan langsung",
        "konten": (
            "Editor View adalah mode tampilan untuk pengembang yang bekerja langsung di kode:\n"
            "- **Fokus utama:** penulisan dan pengeditan kode secara manual.\n"
            "- **Tampilan antarmuka:** IDE tradisional (berbasis VS Code).\n"
            "- **Interaksi agen AI:** bantuan per baris kode dan perbaikan langsung."
        ),
        "sumber": "Infografis",
    },
    {
        "kode": "AG-08",
        "topik": "Mode Tampilan",
        "judul": "Manager View",
        "kata_kunci": "manager view tampilan manajer dashboard dasbor pusat kontrol pengawasan "
                      "koordinasi makro delegasi tugas besar otomatisasi paralel",
        "konten": (
            "Manager View adalah mode tampilan untuk mengelola agen:\n"
            "- **Fokus utama:** pengawasan dan koordinasi agen AI secara makro.\n"
            "- **Tampilan antarmuka:** dasbor pusat kontrol mandiri.\n"
            "- **Interaksi agen AI:** pendelegasian tugas besar dan otomatisasi paralel."
        ),
        "sumber": "Infografis",
    },
    {
        "kode": "AG-09",
        "topik": "Mode Tampilan",
        "judul": "Perbandingan Editor View vs Manager View",
        "kata_kunci": "perbandingan beda perbedaan bandingkan editor view manager view versus vs "
                      "mode tampilan interaksi pengembang",
        "konten": (
            "Perbandingan mode tampilan interaksi pengembang:\n\n"
            "| Aspek | Editor View | Manager View |\n"
            "|---|---|---|\n"
            "| Fokus utama | Penulisan & pengeditan kode manual | Pengawasan & koordinasi agen AI secara makro |\n"
            "| Tampilan antarmuka | IDE tradisional (berbasis VS Code) | Dasbor pusat kontrol mandiri |\n"
            "| Interaksi agen AI | Bantuan baris kode & perbaikan langsung | Delegasi tugas besar & otomatisasi paralel |\n\n"
            "Singkatnya, Editor View cocok saat pengembang ingin memegang kode sendiri, sedangkan "
            "Manager View cocok saat pengembang berperan sebagai manajer yang membagi tugas ke "
            "banyak agen."
        ),
        "sumber": "Infografis",
    },
    {
        "kode": "AG-10",
        "topik": "Kebijakan Otonomi",
        "judul": "3 Tingkat Kebijakan Otonomi",
        "kata_kunci": "tiga tingkat kebijakan otonomi level mode off auto turbo izin kontrol "
                      "keamanan eksekusi moda",
        "konten": (
            "Antigravity 2.0 punya 3 tingkat kebijakan otonomi yang mengatur seberapa bebas agen "
            "bertindak:\n"
            "1. **Mode Off** – agen hanya memberi saran; eksekusi dilakukan manual oleh pengembang.\n"
            "2. **Mode Auto** – agen menjalankan eksekusi yang dinilai aman secara otomatis.\n"
            "3. **Mode Turbo** – otomatisasi eksekusi penuh oleh agen."
        ),
        "sumber": "Infografis",
    },
    {
        "kode": "AG-11",
        "topik": "Kebijakan Otonomi",
        "judul": "Mode Off",
        "kata_kunci": "mode off moda off mati saran manual tanpa eksekusi otomatis kontrol penuh",
        "konten": (
            "Mode Off adalah tingkat otonomi terendah: agen hanya memberikan **saran manual**. "
            "Semua tindakan tetap dieksekusi sendiri oleh pengembang. Mode ini cocok untuk kode "
            "yang sensitif atau saat pengembang ingin kontrol penuh."
        ),
        "sumber": "Infografis",
    },
    {
        "kode": "AG-12",
        "topik": "Kebijakan Otonomi",
        "judul": "Mode Auto",
        "kata_kunci": "mode auto moda auto otomatis eksekusi aman tengah seimbang",
        "konten": (
            "Mode Auto adalah tingkat otonomi menengah: agen boleh menjalankan **eksekusi yang aman** "
            "secara otomatis. Tindakan yang berisiko tetap memerlukan persetujuan pengembang. Mode "
            "ini menyeimbangkan kecepatan dan keamanan."
        ),
        "sumber": "Infografis",
    },
    {
        "kode": "AG-13",
        "topik": "Kebijakan Otonomi",
        "judul": "Mode Turbo",
        "kata_kunci": "mode turbo moda turbo otomatisasi penuh eksekusi penuh cepat otonom penuh",
        "konten": (
            "Mode Turbo adalah tingkat otonomi tertinggi: **otomatisasi eksekusi penuh**. Agen "
            "menjalankan langkah-langkah tanpa menunggu persetujuan satu per satu. Mode ini paling "
            "cepat, tetapi sebaiknya dipakai di lingkungan yang aman (misalnya proyek uji coba) dan "
            "hasilnya tetap diperiksa lewat Artifacts."
        ),
        "sumber": "Infografis",
    },
    {
        "kode": "AG-14",
        "topik": "Penjelasan Tambahan",
        "judul": "Alur Kerja End-to-End dengan Antigravity",
        "kata_kunci": "alur kerja workflow langkah tahapan proses cara kerja bagaimana bekerja "
                      "perancangan pengujian end to end contoh penggunaan",
        "konten": (
            "Berdasarkan komponen di infografis, alur kerja end-to-end dapat digambarkan sebagai "
            "berikut:\n"
            "1. **Atur tim agen** lewat agents.md dan skills.md.\n"
            "2. **Pilih tingkat otonomi** (Off, Auto, atau Turbo).\n"
            "3. **Delegasikan tugas** dari Manager View / Desktop Agent Manager, atau kerjakan detail "
            "kode di Editor View / IDE.\n"
            "4. **Agen mengeksekusi** perancangan, penulisan kode, hingga pengujian (bisa paralel).\n"
            "5. **Verifikasi hasil** melalui Artifacts: dokumen rencana, tangkapan layar, dan rekaman "
            "pengujian.\n"
            "6. Untuk otomatisasi rutin di server, gunakan **CLI dan SDK**."
        ),
        "sumber": "Penjelasan tambahan",
    },
    {
        "kode": "AG-15",
        "topik": "Penjelasan Tambahan",
        "judul": "Perbedaan dengan Asisten Kode Tradisional & Manfaatnya",
        "kata_kunci": "manfaat keunggulan kelebihan perbedaan asisten kode autocomplete copilot "
                      "tradisional mengapa penting dampak produktivitas peran developer",
        "konten": (
            "Asisten kode tradisional umumnya membantu per baris (melengkapi atau memperbaiki kode). "
            "Antigravity 2.0 menggeser peran pengembang menjadi **pengarah dan pengawas agen**: "
            "tugas besar didelegasikan, beberapa agen bekerja paralel, dan hasilnya dibuktikan lewat "
            "Artifacts. Manfaat yang ditawarkan antara lain produktivitas lebih tinggi, pekerjaan "
            "paralel lintas proyek, fleksibilitas (IDE, ekstensi, CLI/SDK), serta kendali risiko "
            "melalui tingkat otonomi Off/Auto/Turbo."
        ),
        "sumber": "Penjelasan tambahan",
    },
    {
        "kode": "AG-16",
        "topik": "Penjelasan Tambahan",
        "judul": "Tantangan dan Tips Penggunaan yang Aman",
        "kata_kunci": "tantangan risiko kekurangan kelemahan keamanan tips aman saran best practice "
                      "praktik terbaik hati hati",
        "konten": (
            "Hal yang perlu diperhatikan saat memakai platform agen semi-otonom:\n"
            "- Semakin tinggi otonomi (Turbo), semakin penting pengawasan; mulai dari Mode Off/Auto.\n"
            "- Selalu periksa Artifacts (rencana, tangkapan layar, rekaman uji) sebelum menerima hasil.\n"
            "- Tulis agents.md dan skills.md dengan jelas agar agen tidak salah memahami peran.\n"
            "- Pengembang tetap bertanggung jawab atas kualitas dan keamanan kode akhir."
        ),
        "sumber": "Penjelasan tambahan",
    },
]

CONTOH_PERTANYAAN = [
    "Apa itu Google Antigravity 2.0?",
    "Sebutkan 4 pilar utama Antigravity",
    "Apa beda Editor View dan Manager View?",
    "Jelaskan 3 tingkat kebijakan otonomi",
    "Fungsi agents.md dan skills.md?",
    "Bagaimana hasil kerja agen diverifikasi?",
]

# Data uji untuk evaluasi akurasi retrieval (pertanyaan -> kode dokumen yang benar)
DATA_UJI = [
    ("apa sih antigravity itu", "AG-00"),
    ("pilar utama platform ada apa saja", "AG-01"),
    ("fungsi desktop agent manager", "AG-02"),
    ("bisa dipakai di vscode atau jetbrains?", "AG-03"),
    ("editor apa saja yang didukung ekstensinya", "AG-03"),
    ("apa kegunaan CLI dan SDK", "AG-04"),
    ("untuk apa file agents.md", "AG-05"),
    ("apa isi skills.md", "AG-05"),
    ("bagaimana cara memverifikasi hasil kerja agen", "AG-06"),
    ("apa itu artefak dalam antigravity", "AG-06"),
    ("jelaskan editor view", "AG-07"),
    ("apa itu manager view", "AG-08"),
    ("perbedaan editor view dengan manager view", "AG-09"),
    ("tingkat otonomi ada berapa", "AG-10"),
    ("mode turbo itu apa", "AG-13"),
    ("kapan pakai moda off", "AG-11"),
    ("mode auto", "AG-12"),
    ("bagaimana alur kerja dari perancangan sampai pengujian", "AG-14"),
    ("apa kelebihannya dibanding copilot", "AG-15"),
    ("apa risikonya, ada tips aman?", "AG-16"),
]
