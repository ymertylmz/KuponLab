export default {
  async fetch(request, env) {
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Content-Type": "application/json; charset=UTF-8",
    };

    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: corsHeaders,
      });
    }

    const url = new URL(request.url);

    // ANA SAYFA
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

    // API-FOOTBALL TEST
    if (url.pathname === "/test") {
      try {
        if (!env.API_FOOTBALL_KEY) {
          return new Response(
            JSON.stringify({
              ok: false,
              error: "API_FOOTBALL_KEY bulunamadı",
            }),
            {
              status: 500,
              headers: corsHeaders,
            }
          );
        }

        const response = await fetch(
          "https://v3.football.api-sports.io/status",
          {
            method: "GET",
            headers: {
              "x-apisports-key": env.API_FOOTBALL_KEY,
            },
          }
        );

        const data = await response.json();

        return new Response(
          JSON.stringify({
            ok: response.ok,
            status: response.status,
            apiFootball: data,
          }),
          {
            status: response.status,
            headers: corsHeaders,
          }
        );
      } catch (error) {
        return new Response(
          JSON.stringify({
            ok: false,
            error: "API-Football bağlantı hatası",
            message: error.message,
          }),
          {
            status: 500,
            headers: corsHeaders,
          }
        );
      }
    }

    // MAÇLARI GETİR
    if (url.pathname === "/matches") {
      try {
        const date = url.searchParams.get("date");

        if (!date) {
          return new Response(
            JSON.stringify({
              ok: false,
              error: "Tarih eksik",
              example: "/matches?date=2026-09-06",
            }),
            {
              status: 400,
              headers: corsHeaders,
            }
          );
        }

        if (!env.API_FOOTBALL_KEY) {
          return new Response(
            JSON.stringify({
              ok: false,
              error: "API_FOOTBALL_KEY bulunamadı",
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

        const response = await fetch(apiUrl, {
          method: "GET",
          headers: {
            "x-apisports-key": env.API_FOOTBALL_KEY,
          },
        });

        const data = await response.json();

        if (!response.ok) {
          return new Response(
            JSON.stringify({
              ok: false,
              error: "API-Football hata döndürdü",
              status: response.status,
              details: data,
            }),
            {
              status: response.status,
              headers: corsHeaders,
            }
          );
        }

        const fixtures = Array.isArray(data.response)
          ? data.response
          : [];

        const matches = fixtures.map((item) => ({
          fixture_id: item.fixture?.id ?? null,
          date: item.fixture?.date ?? null,
          timestamp: item.fixture?.timestamp ?? null,

          league: {
            id: item.league?.id ?? null,
            name: item.league?.name ?? "",
            country: item.league?.country ?? "",
            logo: item.league?.logo ?? "",
            season: item.league?.season ?? null,
            round: item.league?.round ?? "",
          },

          home: {
            id: item.teams?.home?.id ?? null,
            name: item.teams?.home?.name ?? "",
            logo: item.teams?.home?.logo ?? "",
          },

          away: {
            id: item.teams?.away?.id ?? null,
            name: item.teams?.away?.name ?? "",
            logo: item.teams?.away?.logo ?? "",
          },

          status: {
            long: item.fixture?.status?.long ?? "",
            short: item.fixture?.status?.short ?? "",
          },

          goals: {
            home: item.goals?.home ?? null,
            away: item.goals?.away ?? null,
          },
        }));

        return new Response(
          JSON.stringify({
            ok: true,
            date: date,
            count: matches.length,
            api_results: data.results ?? 0,
            errors: data.errors ?? {},
            matches: matches,
          }),
          {
            status: 200,
            headers: corsHeaders,
          }
        );
      } catch (error) {
        return new Response(
          JSON.stringify({
            ok: false,
            error: "Maçlar alınamadı",
            message: error.message,
          }),
          {
            status: 500,
            headers: corsHeaders,
          }
        );
      }
    }

    // BULUNAMAYAN ADRES
    return new Response(
      JSON.stringify({
        ok: false,
        error: "Endpoint bulunamadı",
        endpoints: [
          "/",
          "/test",
          "/matches?date=2026-09-06",
        ],
      }),
      {
        status: 404,
        headers: corsHeaders,
      }
    );
  },
};
