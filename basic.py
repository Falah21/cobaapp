import streamlit as st
from datetime import datetime, date
import requests
from streamlit_lottie import st_lottie
from pymongo import MongoClient

# 🌸 CONFIG & ANIMASI
st.set_page_config(page_title="Happy Girlfriend Day 💗", page_icon="💗", layout="centered")

# Fungsi untuk load Lottie
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Lottie heart
lottie_heart = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_j1adxtyb.json")

# 🌸 MongoDB Setup
MONGO_URI = st.secrets["MONGO_URI"]
DB_NAME = st.secrets["DB_NAME"]
COLLECTION_NAME = st.secrets["COLLECTION_NAME"]

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# 💗 CSS Styling & Floating Emoji
st.markdown("""
<style>
body {
    background-color: #fff0f5;
}
h1, h2, h3, h4 {
    color: #cc0066;
    text-align: center;
}
.stButton>button {
    background-color: #ff66a3;
    color: white;
    border-radius: 15px;
    padding: 0.75em 1.5em;
    font-size: 18px;
}
input {
    border-radius: 10px;
}
.center-button {
    display: flex;
    justify-content: center;
    margin-top: 30px;
}
.heart {
  position: fixed;
  top: -10px;
  font-size: 24px;
  animation: float 6s infinite ease-in;
  color: #ff3399;
}
@keyframes float {
  0% {transform: translateY(0);}
  100% {transform: translateY(100vh);}
}
.bg-decor {
    position: fixed;
    bottom: 20px;
    right: 20px;
    opacity: 0.3;
    width: 100px;
}
[data-testid="stAppViewContainer"] {
    background-image: url("https://i.ibb.co/VHscbZM/bg-romantic.jpg");
    background-size: cover;
    background-position: center;
}
</style>
""", unsafe_allow_html=True)

# 💖 Floating Emoji
st.markdown("""
<script>
for (let i = 0; i < 15; i++) {
  let heart = document.createElement("div");
  heart.className = "heart";
  heart.style.left = Math.random() * 100 + "vw";
  heart.innerText = "💖";
  document.body.appendChild(heart);
}
</script>
""", unsafe_allow_html=True)

# 🌹 Mawar dekoratif
st.markdown("""
<img src="https://cdn.pixabay.com/photo/2017/08/30/07/52/roses-2697037_960_720.png" class="bg-decor">
""", unsafe_allow_html=True)

# Lottie animasi
if lottie_heart:
    st_lottie(lottie_heart, speed=1, height=200, key="love")

# 🌈 State
if "page" not in st.session_state:
    st.session_state.page = "start"

# 💌 Page 1 - Awal
if st.session_state.page == "start":
    st.markdown("""
    <h1 style='text-align: center; color: pink;'>💗 Happy Girlfriend Day 💗</h1>
    <h3 style='text-align: center;'>Apakah kamu siap untuk memulai aplikasi ini?</h3>
    <div class='center-button'>
    """, unsafe_allow_html=True)
    if st.button("💘 Siap - Mulai 👀"):
        st.session_state.page = "form"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# 💬 Page 2 - Form
elif st.session_state.page == "form":
    st.markdown("## ✨ Isi Data Dulu Yuk ✨")
    name = st.text_input("1. Masukkan nama anda:")
    dob = st.date_input(
        "2. Masukkan tanggal lahir anda:",
        value=date(2000, 1, 1),
        min_value=date(1980, 1, 1),
        max_value=date.today()
    )
    jadian = st.date_input("3. Masukkan tanggal rahasia kita:")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔙 Kembali"):
            st.session_state.page = "start"
            st.rerun()
    with col2:
        if st.button("💌 Kirim"):
            if jadian != date(2024, 3, 22):
                st.error("Tanggal rahasia yang dimasukkin belum tepat, coba diingat lagi yaa 😉")
            else:
                st.session_state.name = name
                st.session_state.dob = dob
                st.session_state.page = "final"

                # ✅ Simpan ke MongoDB
                submission = {
                    "name": name,
                    "dob": str(dob),
                    "jadian": str(jadian),
                    "timestamp": datetime.now().isoformat()
                }
                collection.insert_one(submission)
                st.rerun()

# 🥰 Page 3 - Final Ucapan
elif st.session_state.page == "final":
    # Musik
    st.markdown("""
    <audio autoplay loop>
      <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
    </audio>
    """, unsafe_allow_html=True)

    st.markdown(f"## 🥳 Selamat Happy Girlfriend Day, {st.session_state.name}! 🥳")
    st.markdown("""
    ### 💕 1 Agustus 2025 💕  
    Hari ini spesial banget karena ini hari untuk merayakan betapa berharganya adee!  
    Terima kasih sudah selalu sabar, perhatian, dan menjadi seseorang yang sangat berarti buat aa.  
    Happy teruss yaa dee.....🐣  
    """)

    st.markdown("### 📸 Secuil foto-foto adee hahahahaha:")

    col1, col2 = st.columns(2)
    with col1:
        st.image("foto 2.jpg", caption="Lucu banget pake kacamataa 😆", use_container_width=True)
    with col2:
        st.image("foto 1.jpg", caption="Ahahaha apalagi inii cobain kacamata2 😀", use_container_width=True)

    st.markdown("---")
    st.markdown("### 🌷 Tetap jadi diri adee sendirii yaa... 💌")
    st.markdown("**Dari seseorang yang selalu sayang adee, setiap hari, walaupun sering bikin gamudd hahahaha.**")

    if st.button("🔙 Kembali ke Halaman Awal"):
        st.session_state.page = "start"
        st.rerun()
