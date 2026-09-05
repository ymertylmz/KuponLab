import streamlit as st
import requests
from datetime import date, datetime
from zoneinfo import ZoneInfo
import textwrap

# =========================================================
# KUPONLAB V2
# =========================================================

st.set_page_config(
    page_title="KuponLab",
    page_icon="⚽",
    layout="centered"
)

API_BASE = "https://v3.football.api-sports.io"

# =========================================================
# 40 LİG
# 32 ZASLUGABET ANA LİG
# + 5 EK LİG
# + 3 UEFA KUPASI
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

    # 5 EK LİG
    141: "🇪🇸 İspanya - La Liga 2",
    197: "🇬🇷 Yunanistan - Super League",
    169: "🇨🇳 Çin - Super League",
    253: "🇺🇸 ABD - MLS",
    43: "🏴 İngiltere - National League",

    # UEFA
    2: "🏆 UEFA Şampiyonlar Ligi",
    3: "🏆 UEFA Avrupa Ligi",
    848: "🏆 UEFA Konferans Ligi",
}

ALLOWED_LEAGUE_IDS = set(LEAGUES.keys())

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background: #07111f;
    color: white;
}

.block-container {
    max-width: 780px;
    padding-top: 1.2rem;
    padding-bottom: 5rem;
}

h1, h2, h3 {
    color: white !important;
}

.logo {
    text-align: center;
    margin-bottom: 22px;
}

.logo-title {
    font-size: 42px;
    font-weight: 900;
    letter-spacing: -1px;
}

.logo-green {
    color: #38e078;
}

.logo-sub {
    color: #8798ab;
    font-size: 17px;
    margin-top: -5px;
}

.statbox {
    background: #0d1a2a;
    border: 1px solid #1d344b;
    border-radius: 16px;
    padding: 14px;
    text-align: center;
    margin-bottom: 15px;
}

.match-card {
    background: linear-gradient(
        145deg,
        #101d2d,
        #0c1725
    );
    border: 1px solid #20354a;
    border-radius: 18px;
    padding: 17px;
    margin-bottom: 13px;
}

.rank {
    color: #6f849a;
    font-size: 12px;
    font-weight: 700;
}

.league {
    color: #8ea0b3;
    font-size: 12px;
    margin-top: 3px;
}

.match-name {
    color: white;
    font-size: 17px;
    font-weight: 800;
    margin-top: 7px;
}

.market {
    color: #38e078;
    font-size: 18px;
    font-weight: 900;
    margin-top: 12px;
}

.score-green {
    color: #38e078;
    font-size: 25px;
    font-weight: 900;
}

.score-yellow {
    color: #ffd15a;
    font-size: 25px;
    font-weight: 900;
}

.score-orange {
    color: #ff9d4d;
    font-size: 25px;
    font-weight: 900;
}

.score-red {
    color: #ff6868;
    font-size: 25px;
    font-weight: 900;
}

.coupon-safe {
    background: #10281d;
    border: 1px solid #276944;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 14px;
}

.coupon-main {
    background: #29220f;
    border: 1px solid #705b20;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 14px;
}

.coupon-bomb {
    background: #291518;
    border: 1px solid #71383e;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 14px;
}

.coupon-row {
    border-top: 1px solid rgba(255,255,255,.09);
    padding-top: 9px;
    margin-top: 9px;
}

div.stButton > button {
    width: 100%;
    background: #38e078;
    color: #04140b;
    border: none;
    font-weight: 900;
    font-size: 17px;
    border-radius: 14px;
    min-height: 52px;
}

div.stButton > button:hover {
    background: #4cef88;
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
    <div class="logo">
        <div class="logo-title">
            ⚽ Kupon<span class="logo-green">Lab</span>
        </div>
        <div class="logo-sub">
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
    st.info(
        "API-Football key'i gir. "
        "Sonra tarihi seçip taramayı başlat."
    )
    st.stop()

# =========================================================
# API FONKSİYONU
# =========================================================

@st.cache_data(ttl=900, show_spinner=False)
def api_get(endpoint, params, api_key):

    try:

        response = requests.get(
            API_BASE + endpoint,
            headers={
                "x-apisports-key": api_key
            },
            params=params,
            timeout=25
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
            "data": {
                "error": str(e)
            }
        }


# =========================================================
# TAKIM SON 5
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

    fixtures = result["data"].get(
        "response",
        []
    )

    if not fixtures:
        return None

    gf_list = []
    ga_list = []

    over15 = 0
    over25 = 0
    over35 = 0
    btts = 0

    wins = 0
    draws = 0
    losses = 0

    scored_matches = 0
    conceded_matches = 0

    first_half_goals = 0

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

        if total >= 2:
            over15 += 1

        if total >= 3:
            over25 += 1

        if total >= 4:
            over35 += 1

        if gf > 0 and ga > 0:
            btts += 1

        if gf > 0:
            scored_matches += 1

        if ga > 0:
            conceded_matches += 1

        if gf > ga:
            wins += 1

        elif gf == ga:
            draws += 1

        else:
            losses += 1

        halftime = fixture.get(
            "score",
            {}
        ).get(
            "halftime",
            {}
        )

        hth = halftime.get("home")
        hta = halftime.get("away")

        if hth is not None and hta is not None:
            first_half_goals += hth + hta

    played = len(gf_list)

    if played == 0:
        return None

    return {
        "played": played,

        "gf_avg":
            sum(gf_list) / played,

        "ga_avg":
            sum(ga_list) / played,

        "total_goal_avg":
            (
                sum(gf_list) +
                sum(ga_list)
            ) / played,

        "over15":
            over15 / played,

        "over25":
            over25 / played,

        "over35":
            over35 / played,

        "btts":
            btts / played,

        "scored_rate":
            scored_matches / played,

        "conceded_rate":
            conceded_matches / played,

        "win_rate":
            wins / played,

        "draw_rate":
            draws / played,

        "loss_rate":
            losses / played,

        "first_half_goal_avg":
            first_half_goals / played
    }


# =========================================================
# PUAN MOTORU
# =========================================================

def score_limit(value):

    # Artık 100/100 yok.
    return max(
        35,
        min(
            94,
            round(value)
        )
    )


def analyse_match(home, away):

    if not home or not away:
        return None

    # =====================================================
    # 1.5 ÜST
    # =====================================================

    over15_raw = (
        home["over15"] * 26 +
        away["over15"] * 26 +
        home["scored_rate"] * 10 +
        away["scored_rate"] * 10 +
        home["conceded_rate"] * 7 +
        away["conceded_rate"] * 7 +
        min(
            (
                home["total_goal_avg"] +
                away["total_goal_avg"]
            ) / 6,
            1
        ) * 14
    )

    over15 = score_limit(
        48 + over15_raw * 0.46
    )

    # =====================================================
    # 2.5 ÜST
    # =====================================================

    over25_raw = (
        home["over25"] * 30 +
        away["over25"] * 30 +
        home["btts"] * 8 +
        away["btts"] * 8 +
        min(
            (
                home["gf_avg"] +
                away["gf_avg"]
            ) / 3.5,
            1
        ) * 12 +
        min(
            (
                home["total_goal_avg"] +
                away["total_goal_avg"]
            ) / 6,
            1
        ) * 12
    )

    over25 = score_limit(
        44 + over25_raw * 0.48
    )

    # =====================================================
    # KG VAR
    # =====================================================

    btts_raw = (
        home["btts"] * 28 +
        away["btts"] * 28 +
        home["scored_rate"] * 12 +
        away["scored_rate"] * 12 +
        home["conceded_rate"] * 10 +
        away["conceded_rate"] * 10
    )

    btts = score_limit(
        42 + btts_raw * 0.50
    )

    # =====================================================
    # EV SAHİBİ 1X
    # =====================================================

    home_double_raw = (
        home["win_rate"] * 32 +
        home["draw_rate"] * 20 +
        away["loss_rate"] * 28 +
        (
            1 - away["win_rate"]
        ) * 20
    )

    home_double = score_limit(
        44 + home_double_raw * 0.48
    )

    # =====================================================
    # DEPLASMAN X2
    # =====================================================

    away_double_raw = (
        away["win_rate"] * 32 +
        away["draw_rate"] * 20 +
        home["loss_rate"] * 28 +
        (
            1 - home["win_rate"]
        ) * 20
    )

    away_double = score_limit(
        44 + away_double_raw * 0.48
    )

    # =====================================================
    # MARKETLER
    # =====================================================

    markets = {
        "1.5 Üst": over15,
        "2.5 Üst": over25,
        "KG Var": btts,
        "1X": home_double,
        "X2": away_double
    }

    best_market = max(
        markets,
        key=markets.get
    )

    best_score = markets[best_market]

    # İkinci güçlü market
    sorted_markets = sorted(
        markets.items(),
        key=lambda x: x[1],
        reverse=True
    )

    second_market = sorted_markets[1]

    return {
        "market": best_market,
        "score": best_score,
        "second_market": second_market[0],
        "second_score": second_market[1],
        "markets": markets
    }


# =========================================================
# SAAT
# =========================================================

def turkey_time(api_date):

    try:

        dt = datetime.fromisoformat(
            api_date.replace(
                "Z",
                "+00:00"
            )
        )

        dt = dt.astimezone(
            ZoneInfo(
                "Europe/Istanbul"
            )
        )

        return dt.strftime(
            "%H:%M"
        )

    except Exception:

        return "--:--"


# =========================================================
# TARİH
# =========================================================

selected_date = st.date_input(
    "📅 Analiz tarihi",
    value=date.today()
)

with st.expander(
    "🌍 Taranan 40 ligi göster"
):

    for league_id, league_name in LEAGUES.items():

        st.write(
            f"{league_name}  •  ID {league_id}"
        )


scan = st.button(
    "🔍 GÜNÜ TARA"
)

# =========================================================
# TARAMA
# =========================================================

if scan:

    # =====================================================
    # GÜNÜN BÜTÜN MAÇLARINI TEK İSTEKLE AL
    # =====================================================

    with st.spinner(
        "⚽ Günün maçları getiriliyor..."
    ):

        result = api_get(
            "/fixtures",
            {
                "date":
                    selected_date.strftime(
                        "%Y-%m-%d"
                    ),

                "timezone":
                    "Europe/Istanbul"
            },
            api_key
        )

    if not result["ok"]:

        st.error(
            f"API bağlantı hatası: "
            f"{result['status']}"
        )

        st.json(
            result["data"]
        )

        st.stop()

    api_errors = result["data"].get(
        "errors",
        {}
    )

    if api_errors:

        st.error(
            "API-Football hata döndürdü."
        )

        st.json(
            api_errors
        )

        st.stop()

    all_fixtures = result[
        "data"
    ].get(
        "response",
        []
    )

    # =====================================================
    # SADECE 40 LİG
    # =====================================================

    fixtures = []

    for fixture in all_fixtures:

        league_id = fixture[
            "league"
        ][
            "id"
        ]

        if league_id not in ALLOWED_LEAGUE_IDS:
            continue

        status = fixture[
            "fixture"
        ][
            "status"
        ][
            "short"
        ]

        # İptal / ertelenmiş maçları alma
        if status in [
            "CANC",
            "PST",
            "ABD",
            "AWD",
            "WO"
        ]:
            continue

        fixtures.append(
            fixture
        )

    # =====================================================
    # ÖZET
    # =====================================================

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            f"""
            <div class="statbox">
                <b>🌍 Toplam maç</b><br>
                <span style="font-size:25px">
                    {len(all_fixtures)}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            f"""
            <div class="statbox">
                <b>🎯 40 ligde</b><br>
                <span style="
                    font-size:25px;
                    color:#38e078
                ">
                    {len(fixtures)}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    if not fixtures:

        st.warning(
            "Seçilen tarihte bizim 40 ligimizde maç bulunamadı."
        )

        st.stop()

    # =====================================================
    # ANALİZ
    # =====================================================

    analysed = []

    progress = st.progress(0)

    status_text = st.empty()

    total = len(fixtures)

    for index, fixture in enumerate(
        fixtures
    ):

        home = fixture[
            "teams"
        ][
            "home"
        ]

        away = fixture[
            "teams"
        ][
            "away"
        ]

        league = fixture[
            "league"
        ]

        status_text.write(
            f"🧠 {index + 1}/{total} "
            f"{home['name']} - "
            f"{away['name']}"
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
                "fixture_id":
                    fixture[
                        "fixture"
                    ][
                        "id"
                    ],

                "home":
                    home["name"],

                "away":
                    away["name"],

                "league_id":
                    league["id"],

                "league":
                    LEAGUES.get(
                        league["id"],
                        league["name"]
                    ),

                "time":
                    turkey_time(
                        fixture[
                            "fixture"
                        ][
                            "date"
                        ]
                    ),

                "market":
                    analysis["market"],

                "score":
                    analysis["score"],

                "second_market":
                    analysis[
                        "second_market"
                    ],

                "second_score":
                    analysis[
                        "second_score"
                    ],

                "markets":
                    analysis["markets"],

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

    if not analysed:

        st.warning(
            "Maçlar bulundu ancak yeterli geçmiş veriyle analiz yapılamadı."
        )

        st.stop()

    # =====================================================
    # SIRALA
    # =====================================================

    analysed.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    top10 = analysed[:10]

    # =====================================================
    # TOP 10
    # =====================================================

    st.markdown(
        "## 🏆 Günün En İyi 10 Seçimi"
    )

    for rank, match in enumerate(
        top10,
        1
    ):

        score = match["score"]

        if score >= 86:

            icon = "🔥"
            score_class = "score-green"
            grade = "ÇOK GÜÇLÜ"

        elif score >= 80:

            icon = "🟢"
            score_class = "score-green"
            grade = "GÜÇLÜ"

        elif score >= 74:

            icon = "🟡"
            score_class = "score-yellow"
            grade = "İYİ"

        elif score >= 68:

            icon = "🟠"
            score_class = "score-orange"
            grade = "ORTA"

        else:

            icon = "🔴"
            score_class = "score-red"
            grade = "RİSKLİ"

        card = f"""
        <div class="match-card">

            <div class="rank">
                #{rank} • {match['time']}
            </div>

            <div class="league">
                {match['league']}
            </div>

            <div class="match-name">
                {match['home']}
                <br>
                {match['away']}
            </div>

            <div class="market">
                {icon} {match['market']}
            </div>

            <div class="{score_class}">
                {score}/100
            </div>

            <div style="
                color:#91a2b4;
                font-size:12px;
            ">
                {grade}
                • 2. seçenek:
                {match['second_market']}
                {match['second_score']}/100
            </div>

        </div>
        """

        st.markdown(
            textwrap.dedent(card),
            unsafe_allow_html=True
        )

        with st.expander(
            f"📊 #{rank} Detaylı analiz"
        ):

            h = match["home_form"]
            a = match["away_form"]

            col1, col2 = st.columns(2)

            with col1:

                st.markdown(
                    f"### 🏠 {match['home']}"
                )

                st.write(
                    f"Gol ortalaması: "
                    f"**{h['gf_avg']:.2f}**"
                )

                st.write(
                    f"Yediği gol: "
                    f"**{h['ga_avg']:.2f}**"
                )

                st.write(
                    f"1.5 Üst: "
                    f"**%{h['over15'] * 100:.0f}**"
                )

                st.write(
                    f"2.5 Üst: "
                    f"**%{h['over25'] * 100:.0f}**"
                )

                st.write(
                    f"KG Var: "
                    f"**%{h['btts'] * 100:.0f}**"
                )

            with col2:

                st.markdown(
                    f"### ✈️ {match['away']}"
                )

                st.write(
                    f"Gol ortalaması: "
                    f"**{a['gf_avg']:.2f}**"
                )

                st.write(
                    f"Yediği gol: "
                    f"**{a['ga_avg']:.2f}**"
                )

                st.write(
                    f"1.5 Üst: "
                    f"**%{a['over15'] * 100:.0f}**"
                )

                st.write(
                    f"2.5 Üst: "
                    f"**%{a['over25'] * 100:.0f}**"
                )

                st.write(
                    f"KG Var: "
                    f"**%{a['btts'] * 100:.0f}**"
                )

            st.markdown(
                "#### 🎯 Market Puanları"
            )

            for market, market_score in sorted(
                match["markets"].items(),
                key=lambda x: x[1],
                reverse=True
            ):

                st.write(
                    f"**{market}:** "
                    f"{market_score}/100"
                )

    # =====================================================
    # KUPON MOTORU
    # =====================================================

    st.markdown(
        "## 🎟️ KuponLab Kuponları"
    )

    # Aynı maçı bir kez kullan
    strong = [
        x for x in analysed
        if x["score"] >= 82
    ][:3]

    main_coupon = [
        x for x in analysed
        if x["score"] >= 75
    ][:5]

    bomb = [
        x for x in analysed
        if x["score"] >= 68
    ][:7]

    def coupon_html(
        title,
        matches,
        css_class
    ):

        if not matches:

            rows = """
            <div style="
                color:#97a6b6;
                margin-top:8px;
            ">
                Bu kupon için yeterli güçlü maç çıkmadı.
            </div>
            """

        else:

            rows = ""

            for item in matches:

                rows += f"""
                <div class="coupon-row">

                    <b>
                        {item['home']}
                        -
                        {item['away']}
                    </b>

                    <br>

                    <span style="
                        color:#38e078;
                        font-weight:800;
                    ">
                        {item['market']}
                    </span>

                    <span style="
                        float:right;
                        font-weight:800;
                    ">
                        {item['score']}/100
                    </span>

                </div>
                """

        html = f"""
        <div class="{css_class}">
            <h3>{title}</h3>
            {rows}
        </div>
        """

        return textwrap.dedent(
            html
        )

    st.markdown(
        coupon_html(
            "🛡️ SAĞLAM KUPON",
            strong,
            "coupon-safe"
        ),
        unsafe_allow_html=True
    )

    st.markdown(
        coupon_html(
            "🔥 ANA KUPON",
            main_coupon,
            "coupon-main"
        ),
        unsafe_allow_html=True
    )

    st.markdown(
        coupon_html(
            "🚀 BOMBA KUPON",
            bomb,
            "coupon-bomb"
        ),
        unsafe_allow_html=True
    )

    st.caption(
        "KuponLab V2 • 40 seçili lig • "
        "Son 5 maç form analizi • "
        "Puanlar istatistiksel sinyaldir, garanti değildir."
    )
