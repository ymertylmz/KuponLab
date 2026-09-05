export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // =========================
    // YARDIMCI: HTML EKRANI
    // =========================
    function page(title, content) {
      return new Response(`
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title}</title>
  <style>
    * { box-sizing: border-box; }

    body {
      margin: 0;
      padding: 25px 16px;
      background: #071321;
      color: #ffffff;
      font-family: -apple-system, BlinkMacSystemFont, Arial, sans-serif;
    }

    .container {
      max-width: 800px;
      margin: auto;
    }

    h1 {
      margin: 10px 0 5px;
      font-size: 34px;
    }

    .green {
      color: #35df7d;
    }

    .sub {
      color: #8da0b5;
      margin-bottom: 25px;
    }

    .card {
      background: #0d1d2e;
      border: 1px solid #20384f;
      border-radius: 18px;
      padding: 18px;
      margin-bottom: 14px;
    }

    .success {
      color: #35df7d;
      font-weight: 800;
      font-size: 20px;
    }

    .error {
      color: #ff6262;
      font-weight: 800;
    }

    .match {
      background: #0d1d2e;
      border: 1px solid #20384f;
      border-radius: 16px;
      padding: 15px;
      margin: 10px 0;
    }

    .league {
      color: #8da0b5;
      font-size: 13px;
      margin-bottom: 7px;
    }

    .teams {
      font-size: 17px;
      font-weight: 700;
    }

    .time {
      color: #35df7d;
      margin-top: 7px;
      font-weight: 700;
    }

    pre {
      white-space: pre-wrap;
      word-break: break-word;
      font-size: 12px;
      color: #c8d4df;
    }
  </style>
</head>

<body>
  <div class="container">
    ${content}
  </div>
</body>
</html>
      `, {
        status: 200,
        headers: {
          "Content-Type": "text/html; charset=UTF-8",
          "Cache-Control": "no-store"
        }
      });
    }


    // =========================
    // ANA SAYFA
    // =========================
    if (url.pathname === "/") {
      return page(
        "KuponLab API",
        `
        <h1>⚽ Kupon<span class="green">Lab</span></h1>

        <div class="sub">
          API kontrol merkezi
        </div>

        <div class="card">
          <div class="success">
            ✅ Worker çalışıyor
          </div>

          <p>API-Football bağlantısını test etmek için:</p>

          <b>/test</b>

          <p>Maçları görmek için:</p>

          <b>/matches?date=2026-09-06</b>
        </div>
        `
      );
    }


    // =========================
    // API FOOTBALL TEST
    // =========================
    if (url.pathname === "/test") {

      if (!env.API_FOOTBALL_KEY) {
        return page(
          "API Hatası",
          `
          <h1>❌ API Key Yok</h1>

          <div class="card">
            <div class="error">
              API_FOOTBALL_KEY bulunamadı.
            </div>

            <p>
              Cloudflare Worker secret kontrol edilmeli.
            </p>
          </div>
          `
        );
      }

      try {

        const response = await fetch(
          "https://v3.football.api-sports.io/status",
          {
            headers: {
              "x-apisports-key": env.API_FOOTBALL_KEY
            }
          }
        );

        const data = await response.json();

        if (!response.ok) {
          return page(
            "API Hatası",
            `
            <h1>❌ API-Football Hatası</h1>

            <div class="card">
              HTTP durum:
              <b>${response.status}</b>
            </div>

            <div class="card">
              <pre>${escapeHtml(JSON.stringify(data, null, 2))}</pre>
            </div>
            `
          );
        }

        return page(
          "API Test",
          `
          <h1>⚽ Kupon<span class="green">Lab</span></h1>

          <div class="card">
            <div class="success">
              ✅ API-FOOTBALL BAĞLANDI
            </div>

            <p>
              Cloudflare → API-Football bağlantısı çalışıyor.
            </p>
          </div>

          <div class="card">
            <pre>${escapeHtml(JSON.stringify(data, null, 2))}</pre>
          </div>
          `
        );

      } catch (error) {

        return page(
          "Bağlantı Hatası",
          `
          <h1>❌ Bağlantı Hatası</h1>

          <div class="card">
            ${escapeHtml(error.message)}
          </div>
          `
        );
      }
    }


    // =========================
    // MAÇLAR
    // =========================
    if (url.pathname === "/matches") {

      const date =
        url.searchParams.get("date") ||
        new Date().toISOString().slice(0, 10);

      if (!env.API_FOOTBALL_KEY) {
        return page(
          "API Key Yok",
          `
          <h1>❌ API Key Yok</h1>

          <div class="card">
            API_FOOTBALL_KEY bulunamadı.
          </div>
          `
        );
      }

      try {

        const apiURL =
          "https://v3.football.api-sports.io/fixtures?date=" +
          encodeURIComponent(date);

        const response = await fetch(apiURL, {
          headers: {
            "x-apisports-key": env.API_FOOTBALL_KEY
          }
        });

        const data = await response.json();

        if (!response.ok) {

          return page(
            "API Hatası",
            `
            <h1>❌ API-Football Hatası</h1>

            <div class="card">
              HTTP: ${response.status}
            </div>

            <div class="card">
              <pre>${escapeHtml(JSON.stringify(data, null, 2))}</pre>
            </div>
            `
          );
        }


        const fixtures =
          Array.isArray(data.response)
            ? data.response
            : [];


        let matchHTML = "";


        for (const match of fixtures) {

          const league =
            match.league?.name || "Lig bilinmiyor";

          const country =
            match.league?.country || "";

          const home =
            match.teams?.home?.name || "?";

          const away =
            match.teams?.away?.name || "?";

          let time = "--:--";

          if (match.fixture?.date) {
            try {
              time =
                new Intl.DateTimeFormat(
                  "tr-TR",
                  {
                    timeZone: "Europe/Istanbul",
                    hour: "2-digit",
                    minute: "2-digit",
                    hour12: false
                  }
                ).format(
                  new Date(match.fixture.date)
                );
            } catch {}
          }


          matchHTML += `
            <div class="match">

              <div class="league">
                ${escapeHtml(country)}
                •
                ${escapeHtml(league)}
              </div>

              <div class="teams">
                ${escapeHtml(home)}
                ⚔️
                ${escapeHtml(away)}
              </div>

              <div class="time">
                🕐 ${escapeHtml(time)}
              </div>

            </div>
          `;
        }


        if (fixtures.length === 0) {

          matchHTML = `
            <div class="card">

              <div class="error">
                ⚠️ API 0 maç döndürdü
              </div>

              <p>
                API-Football cevabı:
              </p>

              <pre>
${escapeHtml(JSON.stringify({
  results: data.results,
  errors: data.errors,
  paging: data.paging
}, null, 2))}
              </pre>

            </div>
          `;
        }


        return page(
          "KuponLab Maçlar",
          `
          <h1>
            ⚽ Kupon<span class="green">Lab</span>
          </h1>

          <div class="sub">
            ${escapeHtml(date)}
          </div>

          <div class="card">

            <div class="success">
              API'den ${fixtures.length} maç geldi
            </div>

          </div>

          ${matchHTML}
          `
        );


      } catch (error) {

        return page(
          "Sunucu Hatası",
          `
          <h1>❌ Hata</h1>

          <div class="card">
            ${escapeHtml(error.message)}
          </div>
          `
        );
      }
    }


    // =========================
    // 404
    // =========================
    return page(
      "Bulunamadı",
      `
      <h1>404</h1>

      <div class="card">
        Bu adres bulunamadı.
      </div>
      `
    );
  }
};


// =========================
// HTML GÜVENLİ YAZDIRMA
// =========================

function escapeHtml(value) {

  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
