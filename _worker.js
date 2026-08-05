// rawmktg — Cloudflare Worker entry (advanced mode, alongside static assets).
//
// The site is served as static assets. This Worker runs ONLY for requests that
// don't match a static file, so normal page/asset traffic is untouched. Its one
// job is the newsletter endpoint:
//
//   POST /api/subscribe  ->  validate email, store in KV, 303 -> /subscribed
//
// SAFETY: every other path (and any error) falls through to env.ASSETS.fetch,
// i.e. the normal static site. This cannot take pages down on its own.
//
// REQUIRES a KV binding named SUBSCRIBERS (Worker -> Settings -> Bindings).
// If the binding is missing the form still "works" for the visitor (they reach
// the thank-you page) but nothing is stored — so make sure the binding exists.

export default {
  async fetch(request, env, ctx) {
    try {
      const url = new URL(request.url);
      if (url.pathname === "/api/subscribe") {
        if (request.method !== "POST") {
          return new Response("Method Not Allowed", {
            status: 405,
            headers: { Allow: "POST", "content-type": "text/plain; charset=utf-8" },
          });
        }
        return await handleSubscribe(request, env, url);
      }
    } catch (e) {
      // Never let the worker break normal browsing — fall through to assets.
    }
    return env.ASSETS.fetch(request);
  },
};

async function handleSubscribe(request, env, url) {
  let email = "";
  let bot = "";

  try {
    const ct = (request.headers.get("content-type") || "").toLowerCase();
    if (ct.includes("application/json")) {
      const body = await request.json();
      email = String(body.email || "").trim().toLowerCase();
      bot = String(body["bot-field"] || "").trim();
    } else {
      // urlencoded or multipart form posts
      const form = await request.formData();
      email = String(form.get("email") || "").trim().toLowerCase();
      bot = String(form.get("bot-field") || "").trim();
    }
  } catch (e) {
    return new Response("Could not read submission.", {
      status: 400,
      headers: { "content-type": "text/plain; charset=utf-8" },
    });
  }

  // Honeypot tripped: a bot filled the hidden field. Act successful, store nothing.
  if (bot) return thanks(url);

  // Basic email validation.
  const valid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) && email.length <= 254;
  if (!valid) {
    return new Response("Please enter a valid email address.", {
      status: 400,
      headers: { "content-type": "text/plain; charset=utf-8" },
    });
  }

  // Store the subscriber (idempotent: keyed by email, re-subscribing just updates).
  try {
    if (env.SUBSCRIBERS) {
      const record = JSON.stringify({
        email,
        ts: new Date().toISOString(),
        ref: request.headers.get("referer") || "",
        ua: request.headers.get("user-agent") || "",
        country: request.headers.get("cf-ipcountry") || "",
      });
      await env.SUBSCRIBERS.put("sub:" + email, record);
    }
  } catch (e) {
    // Storage hiccup shouldn't show the visitor an error — still send them to thanks.
  }

  return thanks(url);
}

function thanks(url) {
  // 303 so the browser switches POST -> GET on the thank-you page.
  return new Response(null, {
    status: 303,
    headers: { Location: new URL("/subscribed", url.origin).toString() },
  });
}
