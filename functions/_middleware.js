// Cloudflare Pages Function — Accept: text/markdown content negotiation.
// Port of the former Netlify Edge Function `md-negotiate`.
// Serves the clean .md twin of a page when a client EXPLICITLY prefers Markdown,
// HTML otherwise. Scoped to "/", "/blogs/*", "/glossary", "/glossary/*".
//
// SAFETY: this middleware is fail-open. A normal browser or Googlebot never sends
// `Accept: text/markdown`, so it always falls through to the normal HTML response.
// Any error is caught and the request is passed through untouched. If you ever want
// to disable it, delete this file — the .md twins remain reachable as static files.

function parseAccept(header) {
  if (!header || !header.trim()) return [{ type: "*/*", q: 1 }];
  return header.split(",").map((s) => s.trim()).filter(Boolean).map((item) => {
    const [type, ...params] = item.split(";").map((s) => s.trim());
    let q = 1;
    for (const p of params) {
      const eq = p.indexOf("=");
      if (eq < 0 || p.slice(0, eq).trim().toLowerCase() !== "q") continue;
      const n = parseFloat(p.slice(eq + 1));
      if (Number.isFinite(n)) q = n;
    }
    return { type: (type || "").toLowerCase(), q };
  });
}

function qualityFor(entries, candidate) {
  const primary = candidate.split("/")[0];
  let bestSpec = -1, bestQ = 0;
  for (const { type, q } of entries) {
    const spec = type === candidate ? 3 : type === `${primary}/*` ? 2 : type === "*/*" ? 1 : -1;
    if (spec < 0) continue;
    if (spec > bestSpec || (spec === bestSpec && q > bestQ)) { bestSpec = spec; bestQ = q; }
  }
  return bestQ;
}

function hasExplicit(entries, candidate) {
  return entries.some((e) => e.type === candidate && e.q > 0);
}

export async function onRequest(context) {
  const { request, next, env } = context;
  try {
    const url = new URL(request.url);
    const path = url.pathname;

    // Only page routes are in scope; assets and .md files handle themselves.
    const inScope = path === "/" || path === "/glossary"
      || path.startsWith("/blogs/") || path.startsWith("/glossary/");
    if (!inScope || path.endsWith(".md") || /\.[a-z0-9]+$/i.test(path)) return next();

    const mdPath = path === "/" ? "/index.md" : path.replace(/\/+$/, "") + ".md";
    const htmlLink = `<${path}>; rel="alternate"; type="text/html"`;
    const mdLink = `<${mdPath}>; rel="alternate"; type="text/markdown"`;

    const accept = parseAccept(request.headers.get("accept") ?? "");
    const mdQ = qualityFor(accept, "text/markdown");
    const htmlQ = qualityFor(accept, "text/html");

    // Neither representation acceptable -> 406.
    if (mdQ === 0 && htmlQ === 0) {
      return new Response("Not Acceptable", {
        status: 406,
        headers: { "Content-Type": "text/plain; charset=utf-8", "Vary": "Accept", "Link": `${htmlLink}, ${mdLink}` },
      });
    }

    // Client explicitly prefers Markdown and ranks it >= HTML -> serve the .md twin.
    if (hasExplicit(accept, "text/markdown") && mdQ >= htmlQ) {
      const mdReq = new Request(new URL(mdPath, url.origin), { headers: { "Accept": "text/markdown" } });
      const mdResp = env && env.ASSETS ? await env.ASSETS.fetch(mdReq) : await fetch(mdReq);
      if (mdResp && mdResp.ok) {
        return new Response(await mdResp.text(), {
          status: 200,
          headers: { "Content-Type": "text/markdown; charset=utf-8", "Vary": "Accept", "Link": htmlLink },
        });
      }
    }

    // Default: HTML, advertising the markdown alternate.
    const resp = await next();
    const out = new Response(resp.body, resp);
    out.headers.set("Vary", "Accept");
    out.headers.append("Link", mdLink);
    return out;
  } catch (e) {
    // Never break a page over content negotiation.
    return next();
  }
}
