import streamlit as st
import requests
from datetime import date, datetime
import time

# =========================================================
# KUPONLAB
# =========================================================

st.set_page_config(
    page_title="KuponLab",
    page_icon="⚽",
    layout="centered"
)

API_BASE = "https://v3.football.api-sports.io"

# =========================================================
# TASARIM
# =========================================================

st.markdown("""
<style>

.stApp {
    background: #07111f;
    color: white;
}

.block-container {
    max-width: 760px;
    padding-top: 1.2rem;
    padding-bottom: 4rem;
}

h1, h2, h3 {
    color: white;
}

.logo {
    text-align:center;
    margin-bottom:25px;
}

.logo-title {
    font-size:42px;
    font-weight:900;
}

.logo-green {
    color:#38e078;
}

.logo-sub {
    color:#8394aa;
    font-size:18px;
}

.card {
    background:#101d2d;
    border:1px solid #20354a;
    border-radius:18px;
    padding:16px;
    margin-bottom:12px;
}

.pick-title {
    font-size:17px;
    font-weight:800;
}

.meta {
    color:#8798ab;
    font-size:13px;
}

.market {
    color:#38e078;
    font-weight:900;
    font-size:17px;
}

.score-big {
    font-size:25px;
    font-weight:900;
}

.green {
    color:#38e078;
}

.yellow {
    color:#ffd255;
}

.red {
    color:#ff6868;
}

.coupon-safe {
    background:#10281d;
    border:1px solid #236440;
    border-radius:18px;
    padding:17px;
    margin-bottom:15px;
}

.coupon-main {
    background:#2a220f;
    border:1px solid #765b18;
    border-radius:18px;
    padding:17px;
    margin-bottom:15px;
}

.coupon-bomb {
    background:#2a1518;
    border:1px solid #70343a;
    border-radius:18px;
    padding:17px;
    margin-bottom:15px;
}

div.stButton > button {
    width:100%;
    background:#38e078;
    color:#04140b;
    border:none;
    font-weight:900;
    font-size:17px;
    border-radius:14px;
    min-height:52px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOGO
# =========================================================

st.markdown("""
<div class="logo">
    <div class="logo-title">
        ⚽ Kupon<span class="logo-green">Lab</span>
    </div>
    <div class="logo-sub">
        Maçı değil, veriyi oyna.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# API KEY
# =========================================================

api_key = st.text_input(
    "🔑 API-Football Key",
    type="password",
    placeholder="API key'i buraya yapıştır"
)

if not api_key:
    st.info("API-Football key'i gir, sonra tarihi seçip taramayı başlat.")
    st.stop()

HEADERS = {
    "x-apisports-key": api_key
}

# =========================================================
# API
# =========================================================

@st.cache_data(ttl=900, show_spinner=False)
def api_get(endpoint, params, key):
    try:
        r = requests.get(
            API_BASE + endpoint,
            headers={"x-apisports-key": key},
            params=params,
            timeout=20
        )

        data = r.json()

        return {
            "ok": r.ok,
            "status": r.status_code,
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


@st.cache_data(ttl=1800, show_spinner=False)
def get_team_form(team_id, api_key):

    result = api_get(
        "/fixtures",
        {
            "team": team_id,
            "last": 5
        },
        api_key
    )

    if not result["ok"]:
        return None

    matches = result["data"].get("response", [])

    if not matches:
        return None

    goals_for = []
    goals_against = []

    over15 = 0
    over25 = 0
    btts = 0
    wins = 0
    draws = 0
    losses = 0

    for m in matches:

        home_id = m["teams"]["home"]["id"]

        home_goals = m["goals"]["home"]
        away_goals = m["goals"]["away"]

        if home_goals is None or away_goals is None:
            continue

        if home_id == team_id:
            gf = home_goals
            ga = away_goals
        else:
            gf = away_goals
            ga = home_goals

        goals_for.append(gf)
        goals_against.append(ga)

        total = gf + ga

        if total >= 2:
            over15 += 1

        if total >= 3:
            over25 += 1

        if gf > 0 and ga > 0:
            btts += 1

        if gf > ga:
            wins += 1
        elif gf == ga:
            draws += 1
        else:
            losses += 1

    played = len(goals_for)

    if played == 0:
        return None

    return {
        "played": played,
        "gf_avg": sum(goals_for) / played,
        "ga_avg": sum(goals_against) / played,
        "over15": over15 / played,
        "over25": over25 / played,
        "btts": btts / played,
        "win_rate": wins / played,
        "draw_rate": draws / played,
        "loss_rate": losses / played
    }

# =========================================================
# ANALİZ MOTORU
# =========================================================

def clamp(value):
    return max(0, min(100, round(value)))


def analyse_match(home_form, away_form):

    if not home_form or not away_form:
        return None

    # -----------------------------------------------------
    # 1.5 ÜST
    # -----------------------------------------------------

    over15_score = clamp(
        (
            home_form["over15"] * 0.35 +
            away_form["over15"] * 0.35 +
            min(
                (
                    home_form["gf_avg"] +
                    home_form["ga_avg"] +
                    away_form["gf_avg"] +
                    away_form["ga_avg"]
                ) / 6,
                1
            ) * 0.30
        ) * 100
    )

    # -----------------------------------------------------
    # 2.5 ÜST
    # -----------------------------------------------------

    over25_score = clamp(
        (
            home_form["over25"] * 0.40 +
            away_form["over25"] * 0.40 +
            min(
                (
                    home_form["gf_avg"] +
                    away_form["gf_avg"]
                ) / 3.5,
                1
            ) * 0.20
        ) * 100
    )

    # -----------------------------------------------------
    # KG VAR
    # -----------------------------------------------------

    btts_score = clamp(
        (
            home_form["btts"] * 0.40 +
            away_form["btts"] * 0.40 +
            min(
                (
                    home_form["gf_avg"] +
                    away_form["gf_avg"]
                ) / 3,
                1
            ) * 0.20
        ) * 100
    )

    # -----------------------------------------------------
    # 1X
    # -----------------------------------------------------

    home_safe = clamp(
        (
            home_form["win_rate"] * 0.55 +
            home_form["draw_rate"] * 0.25 +
            away_form["loss_rate"] * 0.20
        ) * 100
    )

    # -----------------------------------------------------
    # X2
    # -----------------------------------------------------

    away_safe = clamp(
        (
            away_form["win_rate"] * 0.55 +
            away_form["draw_rate"] * 0.25 +
            home_form["loss_rate"] * 0.20
        ) * 100
    )

    markets = {
        "1.5 Üst": over15_score,
        "2.5 Üst": over25_score,
        "KG Var": btts_score,
        "1X": home_safe,
        "X2": away_safe
    }

    best_market = max(
        markets,
        key=markets.get
    )

    return {
        "market": best_market,
        "score": markets[best_market],
        "markets": markets
    }

# =========================================================
# TARİH
# =========================================================

selected_date = st.date_input(
    "📅 Analiz tarihi",
    value=date.today()
)

scan = st.button(
    "🔍 BUGÜNÜ TARA"
)

# =========================================================
# TARAMA
# =========================================================

if scan:

    with st.spinner("Maçlar getiriliyor..."):

        fixture_result = api_get(
            "/fixtures",
            {
                "date": selected_date.strftime("%Y-%m-%d"),
                "timezone": "Europe/Istanbul"
            },
            api_key
        )

    if not fixture_result["ok"]:

        st.error(
            f"API hatası: {fixture_result['status']}"
        )

        st.json(
            fixture_result["data"]
        )

        st.stop()

    api_errors = fixture_result["data"].get(
        "errors",
        {}
    )

    if api_errors:

        st.error("API-Football hata döndürdü:")
        st.json(api_errors)
        st.stop()

    fixtures = fixture_result["data"].get(
        "response",
        []
    )

    st.success(
        f"⚽ {len(fixtures)} maç bulundu."
    )

    if len(fixtures) == 0:

        st.warning(
            "Bu tarihte API hesabının erişebildiği maç bulunamadı."
        )

        st.stop()

    # API kotasını yakmamak için ilk etapta max 40 maç
    fixtures = fixtures[:40]

    analysed = []

    progress = st.progress(0)

    status_text = st.empty()

    total = len(fixtures)

    for i, fixture in enumerate(fixtures):

        home = fixture["teams"]["home"]
        away = fixture["teams"]["away"]
        league = fixture["league"]

        status_text.write(
            f"🧠 Analiz: {home['name']} - {away['name']}"
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

            match_time = fixture["fixture"]["date"]

            try:
                dt = datetime.fromisoformat(
                    match_time.replace("Z", "+00:00")
                )

                time_text = dt.strftime("%H:%M")

            except:
                time_text = "--:--"

            analysed.append({
                "fixture_id": fixture["fixture"]["id"],
                "home": home["name"],
                "away": away["name"],
                "league": league["name"],
                "country": league["country"],
                "time": time_text,
                "market": analysis["market"],
                "score": analysis["score"],
                "markets": analysis["markets"],
                "home_form": home_form,
                "away_form": away_form
            })

        progress.progress(
            (i + 1) / total
        )

    progress.empty()
    status_text.empty()

    # =====================================================
    # SONUÇLAR
    # =====================================================

    analysed = sorted(
        analysed,
        key=lambda x: x["score"],
        reverse=True
    )

    top = analysed[:10]

    st.markdown(
        "## 🏆 Günün En İyi Seçimleri"
    )

    if not top:

        st.warning(
            "Analiz edilebilen yeterli maç bulunamadı."
        )

        st.stop()

    for index, m in enumerate(top, 1):

        if m["score"] >= 80:
            color = "green"
            icon = "🔥"
        elif m["score"] >= 70:
            color = "yellow"
            icon = "🟢"
        else:
            color = "red"
            icon = "🟡"

        st.markdown(
            f"""
            <div class="card">

                <div class="meta">
                    #{index} • {m['country']} • {m['league']} • {m['time']}
                </div>

                <div class="pick-title">
                    {m['home']} - {m['away']}
                </div>

                <br>

                <div class="market">
                    {icon} {m['market']}
                </div>

                <div class="score-big {color}">
                    {m['score']}/100
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        with st.expander(
            "📊 Detaylı analiz"
        ):

            st.write(
                "Ev sahibi son 5:"
            )

            st.json(
                m["home_form"]
            )

            st.write(
                "Deplasman son 5:"
            )

            st.json(
                m["away_form"]
            )

            st.write(
                "Market skorları:"
            )

            st.json(
                m["markets"]
            )

    # =====================================================
    # KUPONLAR
    # =====================================================

    st.markdown(
        "## 🎟️ Otomatik Kuponlar"
    )

    strong = [
        m for m in analysed
        if m["score"] >= 78
    ][:3]

    main_coupon = [
        m for m in analysed
        if m["score"] >= 70
    ][:5]

    bomb = [
        m for m in analysed
        if m["score"] >= 62
    ][:7]

    def coupon_html(
        title,
        coupon,
        css_class
    ):

        rows = ""

        for x in coupon:

            rows += f"""
            <div style="
                margin-top:10px;
                padding-top:10px;
                border-top:1px solid rgba(255,255,255,.08);
            ">

                <b>
                    {x['home']} - {x['away']}
                </b>

                <br>

                <span style="color:#38e078">
                    {x['market']}
                </span>

                <span style="float:right">
                    {x['score']}/100
                </span>

            </div>
            """

        if not coupon:

            rows = """
            <div style="margin-top:10px">
                Yeterli güçlü seçim bulunamadı.
            </div>
            """

        return f"""
        <div class="{css_class}">

            <h3>{title}</h3>

            {rows}

        </div>
        """

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
        "KuponLab V1 • Son 5 maç form verisiyle analiz yapar. "
        "Sonraki sürümde oran, H2H, iç/dış saha, hakem ve daha gelişmiş filtreler eklenecek."
    )
