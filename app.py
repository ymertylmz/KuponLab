import streamlit as st
from datetime import date

st.set_page_config(
    page_title="KuponLab",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================================================
# iPHONE / MOBİL TASARIM
# =========================================================
st.markdown("""
<style>

/* STREAMLIT GEREKSİZ ALANLARI KALDIR */
#MainMenu {
    visibility: hidden !important;
}

header {
    visibility: hidden !important;
    height: 0 !important;
}

footer {
    visibility: hidden !important;
}

.stDeployButton {
    display: none !important;
}

[data-testid="stToolbar"] {
    display: none !important;
}

[data-testid="stDecoration"] {
    display: none !important;
}

[data-testid="stStatusWidget"] {
    display: none !important;
}

/* SAYFA */
html, body, [data-testid="stAppViewContainer"] {
    background: #03111f !important;
}

[data-testid="stAppViewContainer"] {
    min-height: 100vh;
}

[data-testid="stMain"] {
    background: #03111f !important;
}

.block-container {
    padding-top: 8px !important;
    padding-bottom: 25px !important;
    padding-left: 16px !important;
    padding-right: 16px !important;
    max-width: 700px !important;
}

/* LOGO */
.logo-wrap {
    width: 100%;
    display: flex;
    justify-content: center;
    margin: 0 0 8px 0;
}

.logo-wrap img {
    width: min(100%, 360px);
    max-height: 290px;
    object-fit: contain;
    border-radius: 18px;
}

/* YEŞİL ÇİZGİ */
.green-line {
    width: 115px;
    height: 4px;
    margin: 8px auto 16px auto;
    border-radius: 20px;
    background: #16e887;
    box-shadow: 0 0 14px rgba(22,232,135,.55);
}

/* 3 KUTU */
.info-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    margin-bottom: 14px;
}

.info-card {
    min-width: 0;
    height: 105px;
    border: 1px solid #1c405e;
    border-radius: 17px;
    background: #0a1b2c;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 7px 4px;
}

.info-icon {
    font-size: 25px;
    line-height: 1;
    margin-bottom: 8px;
}

.info-title {
    color: white;
    font-size: 14px;
    line-height: 1.15;
    font-weight: 800;
    white-space: nowrap;
}

.info-sub {
    color: #8292a7;
    font-size: 10px;
    line-height: 1.2;
    margin-top: 6px;
}

/* TÜM NORMAL YAZILAR */
label,
[data-testid="stWidgetLabel"] p {
    color: #e7edf5 !important;
}

/* TARİH */
[data-testid="stDateInput"] {
    margin-bottom: 4px !important;
}

[data-testid="stDateInput"] input {
    min-height: 45px !important;
    border-radius: 12px !important;
}

/* EXPANDER */
[data-testid="stExpander"] {
    background: #091b2d !important;
    border: 1px solid #1b3b57 !important;
    border-radius: 14px !important;
    margin-bottom: 7px !important;
}

[data-testid="stExpander"] summary {
    min-height: 46px !important;
    padding-top: 7px !important;
    padding-bottom: 7px !important;
}

[data-testid="stExpander"] summary p {
    color: #e7edf5 !important;
    font-size: 14px !important;
}

/* BUTON */
div.stButton {
    margin-top: 4px !important;
}

div.stButton > button {
    width: 100% !important;
    min-height: 55px !important;
    border: 0 !important;
    border-radius: 16px !important;

    background: linear-gradient(
        135deg,
        #11d978,
        #21f292
    ) !important;

    color: #02140d !important;
    font-size: 18px !important;
    font-weight: 900 !important;

    box-shadow:
        0 8px 24px rgba(20,230,130,.20) !important;
}

div.stButton > button:active {
    transform: scale(.98);
}

/* SONUÇ KUTUSU */
.result-box {
    background: #091b2d;
    border: 1px solid #1c405e;
    border-radius: 15px;
    padding: 14px;
    margin-top: 12px;
    color: white;
}

/* MOBİL */
@media (max-width: 600px) {

    .block-container {
        padding-top: 3px !important;
        padding-left: 13px !important;
        padding-right: 13px !important;
    }

    .logo-wrap img {
        width: 285px !important;
        max-height: 230px !important;
    }

    .green-line {
        margin-top: 3px;
        margin-bottom: 12px;
    }

    .info-grid {
        gap: 6px;
        margin-bottom: 10px;
    }

    .info-card {
        height: 92px;
        border-radius: 14px;
    }

    .info-icon {
        font-size: 22px;
        margin-bottom: 6px;
    }

    .info-title {
        font-size: 12px;
    }

    .info-sub {
        font-size: 9px;
        margin-top: 4px;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOGO
# =========================================================

st.markdown("""
<div class="logo-wrap">
    <img src="https://raw.githubusercontent.com/ymertylmz/KuponLab/main/kuponlab_logo.png">
</div>

<div class="green-line"></div>
""", unsafe_allow_html=True)


# =========================================================
# BİLGİ KARTLARI
# =========================================================

st.markdown("""
<div class="info-grid">

    <div class="info-card">
        <div class="info-icon">📊</div>
        <div class="info-title">40 seçili lig</div>
        <div class="info-sub">Sadece önemli ligler</div>
    </div>

    <div class="info-card">
        <div class="info-icon">🧠</div>
        <div class="info-title">Veri analizi</div>
        <div class="info-sub">Son 5 maç formu</div>
    </div>

    <div class="info-card">
        <div class="info-icon">🎯</div>
        <div class="info-title">Akıllı öneriler</div>
        <div class="info-sub">Gerçekçi marketler</div>
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# TARİH
# =========================================================

selected_date = st.date_input(
    "📅 Analiz tarihi",
    value=date.today()
)


# =========================================================
# LİGLER
# =========================================================

with st.expander("🌍 Taranan 40 ligi göster"):

    st.markdown("""
🇹🇷 Türkiye Süper Lig  
🏴 İngiltere Premier League  
🇪🇸 İspanya LaLiga  
🇩🇪 Almanya Bundesliga  
🇮🇹 İtalya Serie A  
🇫🇷 Fransa Ligue 1  
🇳🇱 Hollanda Eredivisie  
🇵🇹 Portekiz Primeira Liga  
🇧🇪 Belçika Pro League  
🇩🇰 Danimarka Superliga  
🇳🇴 Norveç Eliteserien  
🇸🇪 İsveç Allsvenskan  
🇨🇭 İsviçre Super League  
🇦🇹 Avusturya Bundesliga  
🇬🇷 Yunanistan Super League  
🇨🇿 Çekya 1. Liga  
🇵🇱 Polonya Ekstraklasa  
🇭🇷 Hırvatistan HNL  
🇷🇸 Sırbistan Super Liga  
🇷🇴 Romanya Liga I  
🇭🇺 Macaristan NB I  
🇧🇬 Bulgaristan First League  
🇺🇦 Ukrayna Premier League  
🇸🇰 Slovakya Super Liga  
🇨🇾 Kıbrıs First Division  
🇮🇱 İsrail Ligat Ha'Al  
🇹🇷 Türkiye 1. Lig  
🏴 Championship  
🇩🇪 2. Bundesliga  
🇩🇪 3. Liga  
🇳🇱 Eerste Divisie  
🇧🇪 Challenger Pro League  
🇳🇴 Norveç 1. Division  
🇫🇷 Ligue 2  
🇪🇸 LaLiga 2  
🇮🇹 Serie B  
🏆 UEFA Champions League  
🏆 UEFA Europa League  
🏆 UEFA Conference League  
🌍 FIFA / UEFA seçili maçlar
""")


# =========================================================
# MARKETLER
# =========================================================

with st.expander("🎯 Kullanılan marketleri göster"):

    st.markdown("""
⚽ Maç Sonucu 1 / X / 2  
⚽ Çifte Şans  
⚽ 1.5 Üst  
⚽ 2.5 Üst  
⚽ 3.5 Üst  
⚽ Karşılıklı Gol  
⚽ İlk Yarı Sonucu  
⚽ İlk Yarı 0.5 Üst  
⚽ Ev Sahibi Gol  
⚽ Deplasman Gol
""")


# =========================================================
# TARAMA
# =========================================================

tara = st.button(
    "🔍 GÜNÜ TARA",
    use_container_width=True,
    type="primary"
)


if tara:

    st.markdown(
        f"""
        <div class="result-box">
            <b>⚽ KuponLab taraması başladı</b><br><br>
            📅 Tarih: {selected_date.strftime("%d.%m.%Y")}<br>
            🌍 40 lig taranıyor...<br>
            🧠 Maç verileri analiz ediliyor...
        </div>
        """,
        unsafe_allow_html=True
    )
