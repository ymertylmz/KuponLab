import streamlit as st
import requests
from datetime import date, datetime
from zoneinfo import ZoneInfo

# =========================================================
# KUPONLAB V4
# =========================================================

st.set_page_config(
    page_title="KuponLab",
    page_icon="⚽",
    layout="centered"
)

API_BASE = "https://v3.football.api-sports.io"

# =========================================================
# 40 LİG
# =========================================================

LEAGUES = {
    140: "🇪🇸 İspanya - La Liga",
    39: "🏴 İngiltere - Premier League",
    40: "🏴 İngiltere - Championship",
    135: "🇮🇹 İtalya - Serie A",
    61: "🇫🇷 Fransa - Ligue 1",
    62: "🇫🇷 Fransa - Ligue 2",
    78: "🇩🇪 Almanya - Bundesliga",
    79: "🇩🇪 Almanya - 2. Bundesliga",
    80: "🇩🇪 Almanya - 3. Liga",
    94: "🇵🇹 Portekiz - Primeira Liga",
    203: "🇹🇷 Türkiye - Süper Lig",
    244: "🇫🇮 Finlandiya - Veikkausliiga",
    219: "🇦🇹 Avusturya - 2. Liga",
    119: "🇩🇰 Danimarka - Superliga",
    114: "🇸🇪 İsveç - Superettan",
    103: "🇳🇴 Norveç - Eliteserien",
    218: "🇦🇹 Avusturya - Bundesliga",
    88: "🇳🇱 Hollanda - Eredivisie",
    89: "🇳🇱 Hollanda - Eerste Divisie",
    180: "🏴 İskoçya - Championship",
    106: "🇵🇱 Polonya - Ekstraklasa",
    63: "🇫🇷 Fransa - Ligue 3",
    144: "🇧🇪 Belçika - Pro League",
    357: "🇮🇪 İrlanda - Premier Division",
    408: "🇬🇧 Kuzey İrlanda - Premiership",
    120: "🇩🇰 Danimarka - 1. Division",
    235: "🇷🇺 Rusya - Premier League",
    113: "🇸🇪 İsveç - Allsvenskan",
    41: "🏴 İngiltere - League One",
    42: "🏴 İngiltere - League Two",
    179: "🏴 İskoçya - Premiership",
    207: "🇨🇭 İsviçre - Super League",

    141: "🇪🇸 İspanya - La Liga 2",
    197: "🇬🇷 Yunanistan - Super League 1",
    169: "🇨🇳 Çin - Super League",
    253: "🇺🇸 ABD - MLS",
    43: "🏴 İngiltere - National League",

    2: "🏆 UEFA Şampiyonlar Ligi",
    3: "🏆 UEFA Avrupa Ligi",
    848: "🏆 UEFA Konferans Ligi",
}

ALLOWED_LEAGUE_IDS = set(LEAGUES.keys())

# =========================================================
# MARKET EŞİKLERİ
# =========================================================

MARKET_LIMITS = {
    "2.5 Üst": 74,
    "3.5 Üst": 71,
    "KG Var": 73,
    "MS 1": 72,
    "MS 2": 72,
    "1X": 76,
    "X2": 76,
}

# =========================================================
# TASARIM
# =========================================================

st.markdown("""
<style>
.stApp {
    background: #07111f;
}

.block-container {
    max-width: 780px;
    padding-top: 1rem;
    padding-bottom: 5rem;
}

h1, h2, h3, h4 {
    color: white !important;
}

p, label {
    color: #dce5ee;
}

[data-testid="stExpander"] {
    background: #0d1928;
    border: 1px solid #1d344b;
    border-radius: 16px;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background: #0d1928;
    border-radius: 18px;
}

[data-testid="stMetric"] {
    background: #0d1928;
    border: 1px solid #1d344b;
    border-radius: 15px;
    padding: 12px;
}

div.stButton > button {
    width: 100%;
    background: #38e078;
    color: #04140b;
    border: none;
    border-radius: 14px;
    min-height: 52px;
    font-size: 17px;
    font-weight: 900;
}

div.stButton > button:hover {
    background: #54ec8d;
    color: #04140b;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div style="text-align:center;margin-bottom:25px;">
        <div style="
            font-size:44px;
            font-weight:900;
            color:white;
        ">
            ⚽ Kupon<span style="color:#38e078;">Lab</span>
        </div>

        <div style="
            color:#8798ab;
            font-size:18px;
        ">
            Maçı değil, veriyi oyna.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# API KEY
# =========================================================

api_key = st.text_input(
    "🔑 API-Football Key",
    type="password",
    placeholder="API key'i buraya yapıştır"
)

if not api_key:
    st.info("API key'i gir, sonra tarihi seçip taramayı başlat.")
    st.stop()

# =========================================================
# API
# =========================================================

@st.cache_data(ttl=900, show_spinner=False)
def api_get(endpoint, params, api_key):
    try:
        response = requests.get(
            API_BASE + endpoint,
            headers={"x-apisports-key": api_key},
            params=params,
            timeout=30
        )

        try:
            data = response.json()
        except Exception:
            data = {}

        return {
            "ok": response.ok,
            "status": response.status_code,
            "data": data
        }

    except Exception as e:
        return {
            "ok": False,
            "status": 500,
            "data": {"error": str(e)}
        }

# =========================================================
# TAKIM FORMU
# =========================================================

@st.cache_data(ttl=1800, show_spinner=False)
def get_team_form(team_id, api_key):

    result = api_get(
        "/fixtures",
        {
            "team": team_id,
            "last": 5,
            "status": "FT"
        },
        api_key
    )

    if not result["ok"]:
        return None

    if result["data"].get("errors"):
        return None

    fixtures = result["data"].get("response", [])

    if not fixtures:
        return None

    gf_list = []
    ga_list = []

    over25 = 0
    over35 = 0
    btts = 0

    wins = 0
    draws = 0
    losses = 0

    scored = 0
    conceded = 0

    clean_sheets = 0
    failed_to_score = 0

    for fixture in fixtures:

        home_id = fixture["teams"]["home"]["id"]

        hg = fixture["goals"]["home"]
        ag = fixture["goals"]["away"]

        if hg is None or ag is None:
            continue

        if home_id == team_id:
            gf = hg
            ga = ag
        else:
            gf = ag
            ga = hg

        gf_list.append(gf)
        ga_list.append(ga)

        total = gf + ga

        if total >= 3:
            over25 += 1

        if total >= 4:
            over35 += 1

        if gf > 0 and ga > 0:
            btts += 1

        if gf > 0:
            scored += 1
        else:
            failed_to_score += 1

        if ga > 0:
            conceded += 1
        else:
            clean_sheets += 1

        if gf > ga:
            wins += 1
        elif gf == ga:
            draws += 1
        else:
            losses += 1

    played = len(gf_list)

    if played == 0:
        return None

    return {
        "played": played,

        "gf_avg": sum(gf_list) / played,
        "ga_avg": sum(ga_list) / played,

        "goal_avg":
            (sum(gf_list) + sum(ga_list)) / played,

        "over25": over25 / played,
        "over35": over35 / played,

        "btts": btts / played,

        "scored_rate": scored / played,
        "conceded_rate": conceded / played,

        "clean_sheet_rate": clean_sheets / played,
        "failed_score_rate": failed_to_score / played,

        "win_rate": wins / played,
        "draw_rate": draws / played,
        "loss_rate": losses / played
    }

# =========================================================
# PUAN SINIRI
# =========================================================

def limit_score(value):
    return max(30, min(94, round(value)))

# =========================================================
# ANALİZ MOTORU
# =========================================================

def analyse_match(home, away):

    if not home or not away:
        return None

    # -----------------------------------------------------
    # 2.5 ÜST
    # -----------------------------------------------------

    over25_raw = (
        home["over25"] * 28 +
        away["over25"] * 28 +
        home["btts"] * 8 +
        away["btts"] * 8 +
        home["scored_rate"] * 7 +
        away["scored_rate"] * 7 +
        min(
            (home["goal_avg"] + away["goal_avg"]) / 6.5,
            1
        ) * 14
    )

    over25 = limit_score(
        36 + over25_raw * 0.55
    )

    # -----------------------------------------------------
    # 3.5 ÜST
    # -----------------------------------------------------

    over35_raw = (
        home["over35"] * 32 +
        away["over35"] * 32 +
        home["over25"] * 10 +
        away["over25"] * 10 +
        min(
            (home["goal_avg"] + away["goal_avg"]) / 7,
            1
        ) * 16
    )

    over35 = limit_score(
        33 + over35_raw * 0.56
    )

    # -----------------------------------------------------
    # KG VAR
    # -----------------------------------------------------

    btts_raw = (
        home["btts"] * 28 +
        away["btts"] * 28 +
        home["scored_rate"] * 10 +
        away["scored_rate"] * 10 +
        home["conceded_rate"] * 12 +
        away["conceded_rate"] * 12
    )

    btts = limit_score(
        35 + btts_raw * 0.55
    )

    # -----------------------------------------------------
    # MS 1
    # -----------------------------------------------------

    ms1_raw = (
        home["win_rate"] * 38 +
        away["loss_rate"] * 30 +
        home["scored_rate"] * 10 +
        away["conceded_rate"] * 10 +
        max(
            home["gf_avg"] - away["gf_avg"],
            0
        ) * 6
    )

    ms1 = limit_score(
        34 + ms1_raw * 0.55
    )

    # -----------------------------------------------------
    # MS 2
    # -----------------------------------------------------

    ms2_raw = (
        away["win_rate"] * 38 +
        home["loss_rate"] * 30 +
        away["scored_rate"] * 10 +
        home["conceded_rate"] * 10 +
        max(
            away["gf_avg"] - home["gf_avg"],
            0
        ) * 6
    )

    ms2 = limit_score(
        34 + ms2_raw * 0.55
    )

    # -----------------------------------------------------
    # 1X
    # -----------------------------------------------------

    one_x_raw = (
        home["win_rate"] * 30 +
        home["draw_rate"] * 20 +
        away["loss_rate"] * 25 +
        (1 - away["win_rate"]) * 25
    )

    one_x = limit_score(
        40 + one_x_raw * 0.50
    )

    # -----------------------------------------------------
    # X2
    # -----------------------------------------------------

    x_two_raw = (
        away["win_rate"] * 30 +
        away["draw_rate"] * 20 +
        home["loss_rate"] * 25 +
        (1 - home["win_rate"]) * 25
    )

    x_two = limit_score(
        40 + x_two_raw * 0.50
    )

    markets = {
        "2.5 Üst": over25,
        "3.5 Üst": over35,
        "KG Var": btts,
        "MS 1": ms1,
        "MS 2": ms2,
        "1X": one_x,
        "X2": x_two,
    }

    # =====================================================
    # EŞİĞİ GEÇMEYEN MARKETLERİ AT
    # =====================================================

    qualified = {}

    for market, score in markets.items():

        minimum = MARKET_LIMITS[market]

        if score >= minimum:
            qualified[market] = score

    if not qualified:
        return None

    sorted_markets = sorted(
        qualified.items(),
        key=lambda x: x[1],
        reverse=True
    )

    best_market = sorted_markets[0]

    if len(sorted_markets) >= 2:
        second_market = sorted_markets[1]
    else:
        second_market = ("-", 0)

    return {
        "market": best_market[0],
        "score": best_market[1],

        "second_market": second_market[0],
        "second_score": second_market[1],

        "markets": markets,
        "qualified": qualified
    }

# =========================================================
# TÜRKİYE SAATİ
# =========================================================

def turkey_time(api_date):

    try:
        dt = datetime.fromisoformat(
            api_date.replace("Z", "+00:00")
        )

        dt = dt.astimezone(
            ZoneInfo("Europe/Istanbul")
        )

        return dt.strftime("%H:%M")

    except Exception:
        return "--:--"

# =========================================================
# TARİH
# =========================================================

selected_date = st.date_input(
    "📅 Analiz tarihi",
    value=date.today()
)

with st.expander("🌍 Taranan 40 ligi göster"):

    for league_id, league_name in LEAGUES.items():
        st.write(
            f"{league_name} • ID {league_id}"
        )

with st.expander("🎯 Kullanılan marketleri göster"):

    for market, minimum in MARKET_LIMITS.items():
        st.write(
            f"{market} • minimum {minimum}/100"
        )

scan = st.button("🔍 GÜNÜ TARA")

# =========================================================
# TARAMA
# =========================================================

if scan:

    with st.spinner("⚽ Günün maçları getiriliyor..."):

        result = api_get(
            "/fixtures",
            {
                "date": selected_date.strftime("%Y-%m-%d"),
                "timezone": "Europe/Istanbul"
            },
            api_key
        )

    if not result["ok"]:

        st.error(
            f"API bağlantı hatası: {result['status']}"
        )

        st.json(result["data"])
        st.stop()

    api_errors = result["data"].get("errors", {})

    if api_errors:
        st.error("API-Football hata döndürdü.")
        st.json(api_errors)
        st.stop()

    all_fixtures = result["data"].get(
        "response",
        []
    )

    fixtures = []

    for fixture in all_fixtures:

        league_id = fixture["league"]["id"]

        if league_id not in ALLOWED_LEAGUE_IDS:
            continue

        status = fixture[
            "fixture"
        ][
            "status"
        ][
            "short"
        ]

        if status in [
            "CANC",
            "PST",
            "ABD",
            "AWD",
            "WO"
        ]:
            continue

        fixtures.append(fixture)

    # =====================================================
    # ÖZET
    # =====================================================

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "🌍 Günün toplam maçı",
            len(all_fixtures)
        )

    with c2:
        st.metric(
            "🎯 Bizim 40 ligde",
            len(fixtures)
        )

    if not fixtures:

        st.warning(
            "Bu tarihte bizim 40 ligimizde maç bulunamadı."
        )

        st.stop()

    # =====================================================
    # ANALİZ
    # =====================================================

    analysed = []

    progress = st.progress(0)
    status_text = st.empty()

    total = len(fixtures)

    for index, fixture in enumerate(fixtures):

        home = fixture["teams"]["home"]
        away = fixture["teams"]["away"]
        league = fixture["league"]

        status_text.write(
            f"🧠 {index + 1}/{total} "
            f"{home['name']} - {away['name']}"
        )

        home_form = get_team_form(
            home["id"],
            api_key
        )

        away_form = get_team_form(
            away["id"],
            api_key
        )

        analysis = analyse_match(
            home_form,
            away_form
        )

        if analysis:

            analysed.append({
                "home": home["name"],
                "away": away["name"],

                "league":
                    LEAGUES.get(
                        league["id"],
                        league["name"]
                    ),

                "time":
                    turkey_time(
                        fixture["fixture"]["date"]
                    ),

                "market":
                    analysis["market"],

                "score":
                    analysis["score"],

                "second_market":
                    analysis["second_market"],

                "second_score":
                    analysis["second_score"],

                "markets":
                    analysis["markets"],

                "qualified":
                    analysis["qualified"],

                "home_form":
                    home_form,

                "away_form":
                    away_form
            })

        progress.progress(
            (index + 1) / total
        )

    progress.empty()
    status_text.empty()

    # =====================================================
    # SONUÇ
    # =====================================================

    if not analysed:

        st.warning(
            "Bugün minimum eşikleri geçen maç çıkmadı."
        )

        st.stop()

    analysed.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    top10 = analysed[:10]

    st.metric(
        "✅ Eşiği geçen maç",
        len(analysed)
    )

    # =====================================================
    # TOP 10
    # =====================================================

    st.markdown(
        "## 🏆 Günün En İyi 10 Seçimi"
    )

    for rank, match in enumerate(top10, 1):

        score = match["score"]

        if score >= 88:
            icon = "🔥"
            grade = "ÇOK GÜÇLÜ"

        elif score >= 82:
            icon = "🟢"
            grade = "GÜÇLÜ"

        elif score >= 76:
            icon = "🟡"
            grade = "İYİ"

        else:
            icon = "🟠"
            grade = "SINIRDA"

        with st.container(border=True):

            st.caption(
                f"#{rank} • "
                f"{match['time']} • "
                f"{match['league']}"
            )

            st.markdown(
                f"### {match['home']} - {match['away']}"
            )

            c1, c2 = st.columns([2, 1])

            with c1:

                st.markdown(
                    f"### {icon} {match['market']}"
                )

                st.caption(
                    grade
                )

                if match["second_market"] != "-":

                    st.caption(
                        f"2. seçenek: "
                        f"{match['second_market']} "
                        f"{match['second_score']}/100"
                    )

            with c2:

                st.metric(
                    "KuponLab",
                    f"{score}/100"
                )

        # =================================================
        # DETAY
        # =================================================

        with st.expander(
            f"📊 #{rank} detaylı analiz"
        ):

            home_form = match["home_form"]
            away_form = match["away_form"]

            c1, c2 = st.columns(2)

            with c1:

                st.markdown(
                    f"#### 🏠 {match['home']}"
                )

                st.write(
                    f"Attığı gol: "
                    f"**{home_form['gf_avg']:.2f}**"
                )

                st.write(
                    f"Yediği gol: "
                    f"**{home_form['ga_avg']:.2f}**"
                )

                st.write(
                    f"2.5 Üst: "
                    f"**%{home_form['over25'] * 100:.0f}**"
                )

                st.write(
                    f"3.5 Üst: "
                    f"**%{home_form['over35'] * 100:.0f}**"
                )

                st.write(
                    f"KG Var: "
                    f"**%{home_form['btts'] * 100:.0f}**"
                )

                st.write(
                    f"Galibiyet: "
                    f"**%{home_form['win_rate'] * 100:.0f}**"
                )

            with c2:

                st.markdown(
                    f"#### ✈️ {match['away']}"
                )

                st.write(
                    f"Attığı gol: "
                    f"**{away_form['gf_avg']:.2f}**"
                )

                st.write(
                    f"Yediği gol: "
                    f"**{away_form['ga_avg']:.2f}**"
                )

                st.write(
                    f"2.5 Üst: "
                    f"**%{away_form['over25'] * 100:.0f}**"
                )

                st.write(
                    f"3.5 Üst: "
                    f"**%{away_form['over35'] * 100:.0f}**"
                )

                st.write(
                    f"KG Var: "
                    f"**%{away_form['btts'] * 100:.0f}**"
                )

                st.write(
                    f"Galibiyet: "
                    f"**%{away_form['win_rate'] * 100:.0f}**"
                )

            st.divider()

            st.markdown(
                "#### 🎯 Tüm market skorları"
            )

            sorted_scores = sorted(
                match["markets"].items(),
                key=lambda x: x[1],
                reverse=True
            )

            for market, market_score in sorted_scores:

                minimum = MARKET_LIMITS[market]

                if market_score >= minimum:
                    sign = "✅"
                else:
                    sign = "❌"

                st.write(
                    f"{sign} **{market}:** "
                    f"{market_score}/100 "
                    f"• eşik {minimum}"
                )

    # =====================================================
    # KUPONLAR
    # =====================================================

    st.markdown(
        "## 🎟️ KuponLab Kuponları"
    )

    strong = [
        x for x in analysed
        if x["score"] >= 84
    ][:3]

    main_coupon = [
        x for x in analysed
        if x["score"] >= 78
    ][:5]

    bomb = [
        x for x in analysed
        if x["score"] >= 72
    ][:7]

    def show_coupon(title, matches):

        with st.container(border=True):

            st.markdown(
                f"### {title}"
            )

            if not matches:

                st.caption(
                    "Yeterli güçlü seçim çıkmadı."
                )

                return

            for item in matches:

                st.markdown(
                    f"**{item['home']} - "
                    f"{item['away']}**"
                )

                c1, c2 = st.columns([3, 1])

                with c1:
                    st.write(
                        f"🎯 {item['market']}"
                    )

                with c2:
                    st.write(
                        f"**{item['score']}/100**"
                    )

                st.divider()

    show_coupon(
        "🛡️ SAĞLAM KUPON",
        strong
    )

    show_coupon(
        "🔥 ANA KUPON",
        main_coupon
    )

    show_coupon(
        "🚀 BOMBA KUPON",
        bomb
    )

    st.caption(
        "KuponLab V4 • 40 seçili lig • "
        "7 bahis marketi • "
        "minimum market eşikleri aktif • "
        "son 5 maç form analizi."
    )
