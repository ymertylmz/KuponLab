import streamlit as st
from datetime import date

st.set_page_config(
    page_title="KuponLab",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================
# MOBİL TASARIM
# =========================
st.markdown("""
<style>

/* Streamlit üst/alt gereksiz alanlar */
#MainMenu {display:none !important;}
footer {display:none !important;}

header[data-testid="stHeader"] {
    display:none !important;
}

[data-testid="stToolbar"] {
    display:none !important;
}

[data-testid="stDecoration"] {
    display:none !important;
}

[data-testid="stStatusWidget"] {
    display:none !important;
}

.stDeployButton {
    display:none !important;
}

/* Ana ekran */
html, body {
    background:#03111f !important;
}

[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background:#03111f !important;
}

.block-container {
    max-width:650px !important;
    padding-top:8px !important;
    padding-left:14px !important;
    padding-right:14px !important;
    padding-bottom:40px !important;
}

/* Logo */
[data-testid="stImage"] {
    text-align:center;
}

[data-testid="stImage"] img {
    width:100% !important;
    max-width:300px !important;
    border-radius:18px !important;
    display:block !important;
    margin:auto !important;
}

/* Yeşil ayraç */
.kl-line {
    width:120px;
    height:4px;
    border-radius:20px;
    background:#1bea8b;
    margin:8px auto 14px auto;
    box-shadow:0 0 12px rgba(27,234,139,.6);
}

/* METRIC KARTLARI */
[data-testid="stMetric"] {
    background:#0a1b2c !important;
    border:1px solid #1c405e !important;
    border-radius:15px !important;
    padding:10px 4px !important;
    min-height:90px !important;
    text-align:center !important;
}

[data-testid="stMetricLabel"] {
    justify-content:center !important;
}

[data-testid="stMetricLabel"] p {
    color:#8798ad !important;
    font-size:10px !important;
    text-align:center !important;
}

[data-testid="stMetricValue"] {
    color:white !important;
    font-size:15px !important;
    font-weight:800 !important;
    text-align:center !important;
}

/* Tarih başlığı */
[data-testid="stWidgetLabel"] p {
    color:#e8edf4 !important;
    font-size:14px !important;
}

/* Tarih */
[data-testid="stDateInput"] input {
    min-height:44px !important;
    border-radius:12px !important;
}

/* Expander */
[data-testid="stExpander"] {
    background:#091b2d !important;
    border:1px solid #1c405e !important;
    border-radius:14px !important;
    margin-bottom:7px !important;
}

[data-testid="stExpander"] summary {
    min-height:46px !important;
}

[data-testid="stExpander"] summary p {
    color:#e7edf5 !important;
    font-size:14px !important;
}

/* Ana buton */
div.stButton > button {
    width:100% !important;
    min-height:56px !important;
    border:none !important;
    border-radius:16px !important;
    background:linear-gradient(135deg,#10d979,#20f293) !important;
    color:#02140d !important;
    font-size:18px !important;
    font-weight:900 !important;
    box-shadow:0 8px 25px rgba(20,230,130,.22) !important;
}

div.stButton > button:active {
    transform:scale(.98);
}

/* Mobil */
@media (max-width:600px) {

    .block-container {
        padding-top:4px !important;
        padding-left:12px !important;
        padding-right:12px !important;
    }

    [data-testid="stImage"] img {
        max-width:255px !important;
    }

    [data-testid="stMetric"] {
        min-height:82px !important;
        padding:8px 2px !important;
    }

    [data-testid="stMetricValue"] {
        font-size:13px !important;
    }

    [data-testid="stMetricLabel"] p {
        font-size:9px !important;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================
# LOGO
# =========================
try:
    st.image("kuponlab_logo.png", use_container_width=False)
except:
    st.markdown(
        "<h1 style='text-align:center;color:white;'>⚽ Kupon<span style='color:#19e889'>Lab</span></h1>",
        unsafe_allow_html=True
    )

st.markdown(
    '<div class="kl-line"></div>',
    unsafe_allow_html=True
)


# =========================
# 3 BİLGİ KARTI
# =========================
c1, c2, c3 = st.columns(3, gap="small")

with c1:
    st.metric(
        label="Sadece önemli ligler",
        value="📊 40 Lig"
    )

with c2:
    st.metric(
        label="Son 5 maç formu",
        value="🧠 Analiz"
    )

with c3:
    st.metric(
        label="Gerçekçi marketler",
        value="🎯 Öneriler"
    )


# =========================
# TARİH
# =========================
selected_date = st.date_input(
    "📅 Analiz tarihi",
    value=date.today(),
    format="YYYY/MM/DD"
)


# =========================
# LİGLER
# =========================
with st.expander("🌍 Taranan 40 ligi göster"):

    st.write("🇹🇷 Türkiye Süper Lig")
    st.write("🏴 İngiltere Premier League")
    st.write("🇪🇸 İspanya LaLiga")
    st.write("🇩🇪 Almanya Bundesliga")
    st.write("🇮🇹 İtalya Serie A")
    st.write("🇫🇷 Fransa Ligue 1")
    st.write("🇳🇱 Hollanda Eredivisie")
    st.write("🇵🇹 Portekiz Primeira Liga")
    st.write("🇧🇪 Belçika Pro League")
    st.write("🇩🇰 Danimarka Superliga")
    st.write("🇳🇴 Norveç Eliteserien")
    st.write("🇸🇪 İsveç Allsvenskan")
    st.write("🇨🇭 İsviçre Super League")
    st.write("🇦🇹 Avusturya Bundesliga")
    st.write("🇬🇷 Yunanistan Super League")
    st.write("🇨🇿 Çekya 1. Liga")
    st.write("🇵🇱 Polonya Ekstraklasa")
    st.write("🇭🇷 Hırvatistan HNL")
    st.write("🇷🇸 Sırbistan Super Liga")
    st.write("🇷🇴 Romanya Liga I")
    st.write("🇭🇺 Macaristan NB I")
    st.write("🇧🇬 Bulgaristan First League")
    st.write("🇺🇦 Ukrayna Premier League")
    st.write("🇸🇰 Slovakya Super Liga")
    st.write("🇨🇾 Kıbrıs First Division")
    st.write("🇮🇱 İsrail Ligat Ha'Al")
    st.write("🇹🇷 Türkiye 1. Lig")
    st.write("🏴 Championship")
    st.write("🇩🇪 2. Bundesliga")
    st.write("🇩🇪 3. Liga")
    st.write("🇳🇱 Eerste Divisie")
    st.write("🇧🇪 Challenger Pro League")
    st.write("🇳🇴 Norveç 1. Division")
    st.write("🇫🇷 Ligue 2")
    st.write("🇪🇸 LaLiga 2")
    st.write("🇮🇹 Serie B")
    st.write("🏆 Şampiyonlar Ligi")
    st.write("🏆 Avrupa Ligi")
    st.write("🏆 Konferans Ligi")
    st.write("🌍 Seçili uluslararası maçlar")


# =========================
# MARKETLER
# =========================
with st.expander("🎯 Kullanılan marketleri göster"):

    st.write("⚽ Maç Sonucu 1 / X / 2")
    st.write("⚽ Çifte Şans")
    st.write("⚽ 1.5 Üst")
    st.write("⚽ 2.5 Üst")
    st.write("⚽ 3.5 Üst")
    st.write("⚽ Karşılıklı Gol")
    st.write("⚽ İlk Yarı Sonucu")
    st.write("⚽ İlk Yarı 0.5 Üst")
    st.write("⚽ Ev Sahibi Gol")
    st.write("⚽ Deplasman Gol")


# =========================
# GÜNÜ TARA
# =========================
if st.button(
    "🔍 GÜNÜ TARA",
    use_container_width=True,
    type="primary"
):
    st.success(
        f"⚽ {selected_date.strftime('%d.%m.%Y')} için tarama başlatıldı."
    )

    st.info(
        "🌍 40 lig taranıyor • 🧠 Maç verileri analiz ediliyor..."
    )
