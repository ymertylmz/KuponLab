export default {
  async fetch(request, env) {
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Content-Type": "application/json; charset=UTF-8",
    };

    // CORS
    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: corsHeaders,
      });
    }

    try {
      const url = new URL(request.url);

      // Sağlık kontrolü
      if (url.pathname === "/" || url.pathname === "") {
        return new Response(
          JSON.stringify({
            ok: true,
            app: "KuponLab API",
            message: "API çalışıyor ⚽",
          }),
          {
            status: 200,
            headers: corsHeaders,
          }
        );
      }

      // MAÇLARI GETİR
      // Örnek:
      // /matches?date=2026-09-06
      if (url.pathname === "/matches") {
        const date =
          url.searchParams.get("date") ||
          new Date().toISOString().slice(0, 10);

        if (!env.API_FOOTBALL_KEY) {
          return new Response(
            JSON.stringify({
              ok: false,
              error: "API_FOOTBALL_KEY bulunamadı.",
            }),
            {
              status: 500,
              headers: corsHeaders,
            }
          );
        }

        const apiUrl =
          "https://v3.football.api-sports.io/fixtures?date=" +
          encodeURIComponent(date);

        const apiResponse = await fetch(apiUrl, {
          method: "GET",
          headers: {
            "x-apisports-key": env.API_FOOTBALL_KEY,
          },
        });

        const data = await apiResponse.json();

        if (!apiResponse.ok) {
          return new Response(
            JSON.stringify({
              ok: false,
              error: "API-Football isteği başarısız.",
              status: apiResponse.status,
              details: data,
            }),
            {
              status: apiResponse.status,
              headers: corsHeaders,
            }
          );
        }

        const matches = (data.response || []).map((item) => ({
          fixture_id: item.fixture?.id ?? null,

          date: item.fixture?.date ?? null,
          timestamp: item.fixture?.timestamp ?? null,

          status: {
            long: item.fixture?.status?.long ?? null,
            short: item.fixture?.status?.short ?? null,
            elapsed: item.fixture?.status?.elapsed ?? null,
          },

          league: {
            id: item.league?.id ?? null,
            name: item.league?.name ?? null,
            country: item.league?.country ?? null,
            logo: item.league?.logo ?? null,
            season: item.league?.season ?? null,
            round: item.league?.round ?? null,
          },

          home: {
            id: item.teams?.home?.id ?? null,
            name: item.teams?.home?.name ?? null,
            logo: item.teams?.home?.logo ?? null,
          },

          away: {
            id: item.teams?.away?.id ?? null,
            name: item.teams?.away?.name ?? null,
            logo: item.teams?.away?.logo ?? null,
          },

          goals: {
            home: item.goals?.home ?? null,
            away: item.goals?.away ?? null,
          },
        }));

        return new Response(
          JSON.stringify({
            ok: true,
            date,
            count: matches.length,
            matches,
          }),
          {
            status: 200,
            headers: corsHeaders,
          }
        );
      }

      // Bilinmeyen adres
      return new Response(
        JSON.stringify({
          ok: false,
          error: "Endpoint bulunamadı.",
        }),
        {
          status: 404,
          headers: corsHeaders,
        }
      );
    } catch (error) {
      return new Response(
        JSON.stringify({
          ok: false,
          error: "Sunucu hatası.",
          message: error.message,
        }),
        {
          status: 500,
          headers: corsHeaders,
        }
      );
    }
  },
};
// deploy
