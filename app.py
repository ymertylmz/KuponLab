import streamlit as st
import streamlit.components.v1 as components
import requests
import base64
import statistics
from datetime import date, datetime
from zoneinfo import ZoneInfo
from PIL import Image

# =========================================================
# KUPONLAB V8
# =========================================================

API_BASE = "https://v3.football.api-sports.io"

# =========================================================
# LOGO / SAYFA AYARLARI
# =========================================================

try:
    page_icon = Image.open("kuponlab_logo.png")
except Exception:
    page_icon = "⚽"

st.set_page_config(
    page_title="KuponLab",
    page_icon=page_icon,
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================================================
# iPHONE ANA EKRAN ADI + ICON
# =========================================================

try:
    with open("kuponlab_logo.png", "rb") as f:
        logo_base64 = base64.b64encode(f.read()).decode("utf-8")

    components.html(
        f"""
        <script>
        try {{
            const doc = window.parent.document;

            doc.title = "KuponLab";

            let appleTitle =
                doc.querySelector('meta[name="apple-mobile-web-app-title"]');

            if (!appleTitle) {{
                appleTitle = doc.createElement("meta");
                appleTitle.name = "apple-mobile-web-app-title";
                doc.head.appendChild(appleTitle);
            }}

            appleTitle.content = "KuponLab";

            let capable =
                doc.querySelector('meta[name="apple-mobile-web-app-capable"]');

            if (!capable) {{
                capable = doc.createElement("meta");
                capable.name = "apple-mobile-web-app-capable";
                doc.head.appendChild(capable);
            }}

            capable.content = "yes";

            let status =
                doc.querySelector('meta[name="apple-mobile-web-app-status-bar-style"]');

            if (!status) {{
                status = doc.createElement("meta");
                status.name = "apple-mobile-web-app-status-bar-style";
                doc.head.appendChild(status);
            }}

            status.content = "black-translucent";

            let theme =
                doc.querySelector('meta[name="theme-color"]');

            if (!theme) {{
                theme = doc.createElement("meta");
                theme.name = "theme-color";
                doc.head.appendChild(theme);
            }}

            theme.content = "#07111f";

            doc.querySelectorAll(
                'link[rel="apple-touch-icon"]'
            ).forEach(el => el.remove());

            const appleIcon = doc.createElement("link");
            appleIcon.rel = "apple-touch-icon";
            appleIcon.sizes = "180x180";
            appleIcon.href = "data:image/png;base64,{logo_base64}";
            doc.head.appendChild(appleIcon);

            doc.querySelectorAll(
                'link[rel="icon"], link[rel="shortcut icon"]'
            ).forEach(el => {{
                el.href = "data:image/png;base64,{logo_base64}";
            }});

        }} catch(e) {{}}
        </script>
        """,
        height=0
    )

except Exception:
    pass

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
    218: "🇦🇹 Avusturya - Bundesliga",

    119: "🇩🇰 Danimarka - Superliga",
    120: "🇩🇰 Danimarka - 1. Division",

    114: "🇸🇪 İsveç - Superettan",
    113: "🇸🇪 İsveç - Allsvenskan",

    103: "🇳🇴 Norveç - Eliteserien",

    88: "🇳🇱 Hollanda - Eredivisie",
    89: "🇳🇱 Hollanda - Eerste Divisie",

    180: "🏴 İskoçya - Championship",
    179: "🏴 İskoçya - Premiership",

    106: "🇵🇱 Polonya - Ekstraklasa",

    63: "🇫🇷 Fransa - Ligue 3",

    144: "🇧🇪 Belçika - Pro League",

    357: "🇮🇪 İrlanda - Premier Division",

    408: "🇬🇧 Kuzey İrlanda - Premiership",

    235: "🇷🇺 Rusya - Premier League",

    41: "🏴 İngiltere - League One",
    42: "🏴 İngiltere - League Two",

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
# MARKETLER
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

# KuponLab oran filtresi
MIN_ODD = 1.35
MAX_ODD = 2.00

# =========================================================
# TASARIM
# =========================================================

st.markdown(
    """
<style>

.stApp {
    background:
        radial-gradient(
            circle at top right,
            rgba(56,224,120,.08),
            transparent 28%
        ),
        linear-gradient(
            180deg,
            #07111f 0%,
            #06101c 100%
        );
}

.block-container {
    max-width: 780px;
    padding-top: 4.8rem;
    padding-bottom: 5rem;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

h1,
h2,
h3,
h4 {
    color: white !important;
}

p,
label {
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

[data-testid="stDateInput"] input {
    border-radius: 14px;
}

div.stButton > button {

    width: 100%;

    background:
        linear-gradient(
            90deg,
            #38e078,
            #24dc78
        );

    color: #04140b;

    border: none;

    border-radius: 16px;

    min-height: 58px;

    font-size: 18px;

    font-weight: 900;

    box-shadow:
        0 8px 28px
        rgba(56,224,120,.20);
}

div.stButton > button:hover {

    background: #54ec8d;

    color: #04140b;

    border: none;
}

.green-line {

    width: 110px;

    height: 3px;

    background: #38e078;

    border-radius: 99px;

    margin:
        3px auto
        30px auto;

    box-shadow:
        0 0 12px
        rgba(56,224,120,.5);
}

.feature-wrap {

    display: flex;

    gap: 10px;

    margin-bottom: 30px;
}

.feature-card {

    flex: 1;

    min-width: 0;

    background:
        linear-gradient(
            145deg,
            #0d1c2d,
            #0a1725
        );

    border:
        1px solid #1c3850;

    border-radius: 18px;

    padding:
        16px 6px;

    text-align: center;
}

.feature-icon {

    font-size: 27px;

    margin-bottom: 5px;
}

.feature-title {

    color: white;

    font-size: 13px;

    font-weight: 900;

    line-height: 1.2;
}

.feature-sub {

    color: #8798ab;

    font-size: 10px;

    margin-top: 5px;

    line-height: 1.3;
}

@media (max-width:600px) {

    .block-container {

        padding-top: 4.8rem;

        padding-left: 1rem;

        padding-right: 1rem;
    }

}

</style>
""",
    unsafe_allow_html=True
)

# =========================================================
# GERÇEK LOGO
# =========================================================

try:

    logo = Image.open(
        "kuponlab_logo.png"
    )

    width, height = logo.size

    crop_bottom = int(
        height * 0.84
    )

    logo_crop = logo.crop(
        (
            0,
            0,
            width,
            crop_bottom
        )
    )

    c1, c2, c3 = st.columns(
        [0.06, 0.88, 0.06]
    )

    with c2:

        st.image(
            logo_crop,
            use_container_width=True
        )

except Exception:

    st.markdown(
        "## ⚽ KuponLab"
    )

st.markdown(
    '<div class="green-line"></div>',
    unsafe_allow_html=True
)

# =========================================================
# ÖZELLİKLER
# =========================================================

st.markdown(
    '<div class="feature-wrap">'
    '<div class="feature-card">'
    '<div class="feature-icon">📊</div>'
    '<div class="feature-title">40 seçili lig</div>'
    '<div class="feature-sub">Sadece önemli ligler</div>'
    '</div>'
    '<div class="feature-card">'
    '<div class="feature-icon">🧠</div>'
    '<div class="feature-title">Veri analizi</div>'
    '<div class="feature-sub">Son 5 maç formu</div>'
    '</div>'
    '<div class="feature-card">'
    '<div class="feature-icon">🎯</div>'
    '<div class="feature-title">Akıllı öneriler</div>'
    '<div class="feature-sub">Gerçekçi marketler</div>'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

# =========================================================
# API KEY
# =========================================================

try:

    api_key = st.secrets[
        "API_FOOTBALL_KEY"
    ]

except Exception:

    st.error(
        "API key bulunamadı."
    )

    st.stop()

# =========================================================
# API
# =========================================================

@st.cache_data(
    ttl=900,
    show_spinner=False
)
def api_get(
    endpoint,
    params,
    api_key
):

    try:

        response = requests.get(

            API_BASE + endpoint,

            headers={
                "x-apisports-key":
                    api_key
            },

            params=params,

            timeout=30
        )

        try:

            data = response.json()

        except Exception:

            data = {}

        return {

            "ok":
                response.ok,

            "status":
                response.status_code,

            "data":
                data
        }

    except Exception as e:

        return {

            "ok":
                False,

            "status":
                500,

            "data": {
                "error":
                    str(e)
            }
        }

# =========================================================
# SON 5 MAÇ
# =========================================================

@st.cache_data(
    ttl=1800,
    show_spinner=False
)
def get_team_form(
    team_id,
    api_key
):

    result = api_get(

        "/fixtures",

        {
            "team":
                team_id,

            "last":
                5,

            "status":
                "FT"
        },

        api_key
    )

    if not result["ok"]:
        return None

    if result[
        "data"
    ].get(
        "errors"
    ):
        return None

    fixtures = result[
        "data"
    ].get(
        "response",
        []
    )

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

    for fixture in fixtures:

        home_id = fixture[
            "teams"
        ][
            "home"
        ][
            "id"
        ]

        home_goals = fixture[
            "goals"
        ][
            "home"
        ]

        away_goals = fixture[
            "goals"
        ][
            "away"
        ]

        if (
            home_goals is None
            or
            away_goals is None
        ):
            continue

        if home_id == team_id:

            gf = home_goals
            ga = away_goals

        else:

            gf = away_goals
            ga = home_goals

        gf_list.append(
            gf
        )

        ga_list.append(
            ga
        )

        total = (
            gf +
            ga
        )

        if total >= 3:
            over25 += 1

        if total >= 4:
            over35 += 1

        if (
            gf > 0
            and
            ga > 0
        ):
            btts += 1

        if gf > 0:
            scored += 1

        if ga > 0:
            conceded += 1

        if gf > ga:
            wins += 1

        elif gf == ga:
            draws += 1

        else:
            losses += 1

    played = len(
        gf_list
    )

    if played == 0:
        return None

    return {

        "played":
            played,

        "gf_avg":
            sum(
                gf_list
            ) / played,

        "ga_avg":
            sum(
                ga_list
            ) / played,

        "goal_avg":
            (
                sum(gf_list)
                +
                sum(ga_list)
            ) / played,

        "over25":
            over25 / played,

        "over35":
            over35 / played,

        "btts":
            btts / played,

        "scored_rate":
            scored / played,

        "conceded_rate":
            conceded / played,

        "win_rate":
            wins / played,

        "draw_rate":
            draws / played,

        "loss_rate":
            losses / played
    }

# =========================================================
# PUAN
# =========================================================

def limit_score(
    value
):

    return max(
        30,
        min(
            94,
            round(
                value
            )
        )
    )

# =========================================================
# ANALİZ
# =========================================================

def analyse_match(
    home,
    away
):

    if not home or not away:
        return None

    over25_raw = (

        home["over25"] * 28
        +
        away["over25"] * 28
        +
        home["btts"] * 8
        +
        away["btts"] * 8
        +
        home["scored_rate"] * 7
        +
        away["scored_rate"] * 7
        +
        min(
            (
                home["goal_avg"]
                +
                away["goal_avg"]
            ) / 6.5,
            1
        ) * 14
    )

    over25 = limit_score(
        36
        +
        over25_raw * .55
    )

    over35_raw = (

        home["over35"] * 32
        +
        away["over35"] * 32
        +
        home["over25"] * 10
        +
        away["over25"] * 10
        +
        min(
            (
                home["goal_avg"]
                +
                away["goal_avg"]
            ) / 7,
            1
        ) * 16
    )

    over35 = limit_score(
        33
        +
        over35_raw * .56
    )

    btts_raw = (

        home["btts"] * 28
        +
        away["btts"] * 28
        +
        home["scored_rate"] * 10
        +
        away["scored_rate"] * 10
        +
        home["conceded_rate"] * 12
        +
        away["conceded_rate"] * 12
    )

    btts = limit_score(
        35
        +
        btts_raw * .55
    )

    ms1_raw = (

        home["win_rate"] * 38
        +
        away["loss_rate"] * 30
        +
        home["scored_rate"] * 10
        +
        away["conceded_rate"] * 10
        +
        max(
            home["gf_avg"]
            -
            away["gf_avg"],
            0
        ) * 6
    )

    ms1 = limit_score(
        34
        +
        ms1_raw * .55
    )

    ms2_raw = (

        away["win_rate"] * 38
        +
        home["loss_rate"] * 30
        +
        away["scored_rate"] * 10
        +
        home["conceded_rate"] * 10
        +
        max(
            away["gf_avg"]
            -
            home["gf_avg"],
            0
        ) * 6
    )

    ms2 = limit_score(
        34
        +
        ms2_raw * .55
    )

    one_x_raw = (

        home["win_rate"] * 30
        +
        home["draw_rate"] * 20
        +
        away["loss_rate"] * 25
        +
        (
            1
            -
            away["win_rate"]
        ) * 25
    )

    one_x = limit_score(
        40
        +
        one_x_raw * .50
    )

    x_two_raw = (

        away["win_rate"] * 30
        +
        away["draw_rate"] * 20
        +
        home["loss_rate"] * 25
        +
        (
            1
            -
            home["win_rate"]
        ) * 25
    )

    x_two = limit_score(
        40
        +
        x_two_raw * .50
    )

    markets = {

        "2.5 Üst":
            over25,

        "3.5 Üst":
            over35,

        "KG Var":
            btts,

        "MS 1":
            ms1,

        "MS 2":
            ms2,

        "1X":
            one_x,

        "X2":
            x_two
    }

    qualified = {}

    for (
        market,
        score
    ) in markets.items():

        if (
            score
            >=
            MARKET_LIMITS[
                market
            ]
        ):

            qualified[
                market
            ] = score

    if not qualified:
        return None

    sorted_markets = sorted(

        qualified.items(),

        key=lambda x:
            x[1],

        reverse=True
    )

    best = sorted_markets[
        0
    ]

    if len(
        sorted_markets
    ) >= 2:

        second = sorted_markets[
            1
        ]

    else:

        second = (
            "-",
            0
        )

    return {

        "market":
            best[0],

        "score":
            best[1],

        "second_market":
            second[0],

        "second_score":
            second[1],

        "markets":
            markets
    }

# =========================================================
# MAÇ ÖNCESİ ORANLAR
# =========================================================

@st.cache_data(ttl=10800, show_spinner=False)
def get_fixture_odds(fixture_id, api_key):
    """
    API-Football /odds verisini okur.
    Aynı market için birden fazla bookmaker varsa medyan oranı kullanır.
    """
    result = api_get(
        "/odds",
        {"fixture": fixture_id},
        api_key
    )

    if not result["ok"] or result["data"].get("errors"):
        return {}

    rows = result["data"].get("response", [])
    collected = {
        "2.5 Üst": [],
        "3.5 Üst": [],
        "KG Var": [],
        "MS 1": [],
        "MS 2": [],
        "1X": [],
        "X2": [],
    }

    for row in rows:
        for bookmaker in row.get("bookmakers", []):
            for bet in bookmaker.get("bets", []):
                bet_name = str(bet.get("name", "")).strip().lower()

                for item in bet.get("values", []):
                    value = str(item.get("value", "")).strip().lower()

                    try:
                        odd = float(item.get("odd"))
                    except (TypeError, ValueError):
                        continue

                    market = None

                    if bet_name in ("match winner", "1x2"):
                        if value in ("home", "1"):
                            market = "MS 1"
                        elif value in ("away", "2"):
                            market = "MS 2"

                    elif (
                        "over/under" in bet_name
                        or "goals over" in bet_name
                        or bet_name in ("goals", "total goals")
                    ):
                        if value in ("over 2.5", "over 2,5"):
                            market = "2.5 Üst"
                        elif value in ("over 3.5", "over 3,5"):
                            market = "3.5 Üst"

                    elif (
                        "both teams" in bet_name
                        or "both team" in bet_name
                        or "btts" in bet_name
                    ):
                        if value in ("yes", "evet"):
                            market = "KG Var"

                    elif "double chance" in bet_name:
                        if value in ("home/draw", "1x", "home or draw"):
                            market = "1X"
                        elif value in ("draw/away", "x2", "draw or away"):
                            market = "X2"

                    if market:
                        collected[market].append(odd)

    odds = {}
    for market, values in collected.items():
        if values:
            odds[market] = round(statistics.median(values), 2)

    return odds


def choose_market_with_odds(analysis, odds):
    """
    Yalnızca hem KuponLab eşiğini geçen hem de 1.35-2.00 oran aralığında
    bulunan marketleri değerlendirir. Skor + oran değeriyle en iyiyi seçer.
    """
    candidates = []

    for market, score in analysis["markets"].items():
        odd = odds.get(market)

        if odd is None:
            continue

        if score < MARKET_LIMITS[market]:
            continue

        if not (MIN_ODD <= odd <= MAX_ODD):
            continue

        # Oran yükseldikçe küçük bir değer bonusu ver.
        # Böylece 1.08'lik "çok güvenli" seçimler değil, oynanabilir oranlar öne çıkar.
        value_score = score + min(max(odd - MIN_ODD, 0) * 12, 6)

        candidates.append(
            (market, score, odd, value_score)
        )

    if not candidates:
        return None

    candidates.sort(key=lambda x: (x[3], x[1]), reverse=True)
    best = candidates[0]
    second = candidates[1] if len(candidates) > 1 else None

    return {
        "market": best[0],
        "score": best[1],
        "odd": best[2],
        "value_score": best[3],
        "second_market": second[0] if second else "-",
        "second_score": second[1] if second else 0,
        "second_odd": second[2] if second else None,
    }


# =========================================================
# TÜRKİYE SAATİ
# =========================================================

def turkey_time(
    api_date
):

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

    for (
        league_id,
        league_name
    ) in LEAGUES.items():

        st.write(
            f"{league_name} • ID {league_id}"
        )

with st.expander(
    "🎯 Kullanılan marketleri göster"
):

    for (
        market,
        minimum
    ) in MARKET_LIMITS.items():

        st.write(
            f"{market} • minimum {minimum}/100"
        )

scan = st.button(
    "🔍 GÜNÜ TARA"
)

# =========================================================
# TARAMA
# =========================================================

if scan:

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
            f"API bağlantı hatası: {result['status']}"
        )

        st.json(
            result["data"]
        )

        st.stop()

    api_errors = result[
        "data"
    ].get(
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

    fixtures = []

    for fixture in all_fixtures:

        league_id = fixture[
            "league"
        ][
            "id"
        ]

        if (
            league_id
            not in
            ALLOWED_LEAGUE_IDS
        ):
            continue

        status = fixture[
            "fixture"
        ][
            "status"
        ][
            "short"
        ]

        # Geçmiş / başlamış / bitmiş maçları kupona alma.
        # Bugün taranıyorsa yalnızca Türkiye saatine göre henüz başlamamış maçlar kalır.
        # Gelecek tarihlerde tüm planlanmış maçlar taranır.
        if status in [
            "CANC",
            "PST",
            "ABD",
            "AWD",
            "WO",
            "1H",
            "HT",
            "2H",
            "ET",
            "BT",
            "P",
            "SUSP",
            "INT",
            "FT",
            "AET",
            "PEN",
            "LIVE"
        ]:
            continue

        if selected_date == datetime.now(ZoneInfo("Europe/Istanbul")).date():
            try:
                fixture_dt = datetime.fromisoformat(
                    fixture["fixture"]["date"].replace("Z", "+00:00")
                ).astimezone(ZoneInfo("Europe/Istanbul"))

                now_tr = datetime.now(ZoneInfo("Europe/Istanbul"))

                if fixture_dt <= now_tr:
                    continue
            except Exception:
                # Saat okunamazsa başlamış maçın yanlışlıkla kupona girmemesi için ele.
                continue

        fixtures.append(
            fixture
        )

    c1, c2 = st.columns(
        2
    )

    with c1:

        st.metric(
            "🌍 Günün toplam maçı",
            len(
                all_fixtures
            )
        )

    with c2:

        st.metric(
            "🎯 Bizim 40 ligde",
            len(
                fixtures
            )
        )

    if not fixtures:

        st.warning(
            "Bu tarihte bizim 40 ligimizde maç bulunamadı."
        )

        st.stop()

    analysed = []

    progress = st.progress(
        0
    )

    status_text = st.empty()

    total = len(
        fixtures
    )

    for (
        index,
        fixture
    ) in enumerate(
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
            fixture_odds = get_fixture_odds(
                fixture["fixture"]["id"],
                api_key
            )

            selected = choose_market_with_odds(
                analysis,
                fixture_odds
            )

            # Oranı bulunmayan veya 1.35-2.00 dışında kalan maç kupona girmez.
            if selected:
                analysed.append(
                    {

                        "home":
                            home["name"],

                        "away":
                            away["name"],

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
                            selected["market"],

                        "score":
                            selected["score"],

                        "odd":
                            selected["odd"],

                        "value_score":
                            selected["value_score"],

                        "second_market":
                            selected["second_market"],

                        "second_score":
                            selected["second_score"],

                        "second_odd":
                            selected["second_odd"],

                        "markets":
                            analysis["markets"],

                        "odds":
                            fixture_odds,

                        "home_form":
                            home_form,

                        "away_form":
                            away_form
                    }
                )

        progress.progress(
            (
                index + 1
            )
            /
            total
        )

    progress.empty()
    status_text.empty()

    if not analysed:

        st.warning(
            "Bugün minimum eşikleri geçen maç çıkmadı."
        )

        st.stop()

    analysed.sort(
        key=lambda x:
            x.get("value_score", x["score"]),
        reverse=True
    )

    top10 = analysed[
        :10
    ]

    st.metric(
        "✅ Eşiği geçen maç",
        len(
            analysed
        )
    )

    # =====================================================
    # TOP 10
    # =====================================================

    st.markdown(
        "## 🏆 Günün En İyi 10 Seçimi"
    )

    for (
        rank,
        match
    ) in enumerate(
        top10,
        1
    ):

        score = match[
            "score"
        ]

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

        with st.container(
            border=True
        ):

            st.caption(
                f"#{rank} • "
                f"{match['time']} • "
                f"{match['league']}"
            )

            st.markdown(
                f"### "
                f"{match['home']} "
                f"- "
                f"{match['away']}"
            )

            c1, c2 = st.columns(
                [
                    2,
                    1
                ]
            )

            with c1:

                st.markdown(
                    f"### "
                    f"{icon} "
                    f"{match['market']} • {match['odd']:.2f}"
                )

                st.caption(
                    f"{grade} • Oran filtresi {MIN_ODD:.2f}-{MAX_ODD:.2f}"
                )

                if (
                    match[
                        "second_market"
                    ]
                    !=
                    "-"
                ):

                    second_odd_text = (
                        f" • {match['second_odd']:.2f}"
                        if match.get("second_odd") is not None
                        else ""
                    )

                    st.caption(
                        f"2. seçenek: "
                        f"{match['second_market']} "
                        f"{match['second_score']}/100"
                        f"{second_odd_text}"
                    )

            with c2:

                st.metric(
                    "KuponLab",
                    f"{score}/100"
                )

        with st.expander(
            f"📊 #{rank} detaylı analiz"
        ):

            hf = match[
                "home_form"
            ]

            af = match[
                "away_form"
            ]

            c1, c2 = st.columns(
                2
            )

            with c1:

                st.markdown(
                    f"#### 🏠 "
                    f"{match['home']}"
                )

                st.write(
                    f"Attığı gol: "
                    f"**{hf['gf_avg']:.2f}**"
                )

                st.write(
                    f"Yediği gol: "
                    f"**{hf['ga_avg']:.2f}**"
                )

                st.write(
                    f"2.5 Üst: "
                    f"**%{hf['over25'] * 100:.0f}**"
                )

                st.write(
                    f"3.5 Üst: "
                    f"**%{hf['over35'] * 100:.0f}**"
                )

                st.write(
                    f"KG Var: "
                    f"**%{hf['btts'] * 100:.0f}**"
                )

                st.write(
                    f"Galibiyet: "
                    f"**%{hf['win_rate'] * 100:.0f}**"
                )

            with c2:

                st.markdown(
                    f"#### ✈️ "
                    f"{match['away']}"
                )

                st.write(
                    f"Attığı gol: "
                    f"**{af['gf_avg']:.2f}**"
                )

                st.write(
                    f"Yediği gol: "
                    f"**{af['ga_avg']:.2f}**"
                )

                st.write(
                    f"2.5 Üst: "
                    f"**%{af['over25'] * 100:.0f}**"
                )

                st.write(
                    f"3.5 Üst: "
                    f"**%{af['over35'] * 100:.0f}**"
                )

                st.write(
                    f"KG Var: "
                    f"**%{af['btts'] * 100:.0f}**"
                )

                st.write(
                    f"Galibiyet: "
                    f"**%{af['win_rate'] * 100:.0f}**"
                )

            st.divider()

            st.markdown(
                "#### 🎯 Market skorları"
            )

            scores = sorted(

                match[
                    "markets"
                ].items(),

                key=lambda x:
                    x[1],

                reverse=True
            )

            for (
                market,
                market_score
            ) in scores:

                minimum = MARKET_LIMITS[
                    market
                ]

                mark = (
                    "✅"
                    if
                    market_score
                    >=
                    minimum
                    else
                    "❌"
                )

                market_odd = match.get("odds", {}).get(market)
                odd_text = (
                    f" • oran {market_odd:.2f}"
                    if market_odd is not None
                    else " • oran yok"
                )

                st.write(
                    f"{mark} "
                    f"**{market}:** "
                    f"{market_score}/100 "
                    f"• eşik {minimum}"
                    f"{odd_text}"
                )

    # =====================================================
    # KUPONLAR
    # =====================================================

    st.markdown(
        "## 🎟️ KuponLab Kuponları"
    )

    strong = [
        x
        for x
        in analysed
        if
        x["score"] >= 84
    ][
        :3
    ]

    main_coupon = [
        x
        for x
        in analysed
        if
        x["score"] >= 78
    ][
        :5
    ]

    bomb = [
        x
        for x
        in analysed
        if
        x["score"] >= 72
    ][
        :7
    ]

    def show_coupon(
        title,
        matches
    ):

        with st.container(
            border=True
        ):

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
                    f"**"
                    f"{item['home']} "
                    f"- "
                    f"{item['away']}"
                    f"**"
                )

                c1, c2 = st.columns(
                    [
                        3,
                        1
                    ]
                )

                with c1:

                    st.write(
                        f"🎯 "
                        f"{item['market']}"
                    )

                with c2:

                    st.write(
                        f"**"
                        f"{item['score']}/100"
                        f"**"
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
        "KuponLab V8 • "
        "40 seçili lig • "
        "API key otomatik • "
        "7 bahis marketi • "
        "son 5 maç analizi."
    )
