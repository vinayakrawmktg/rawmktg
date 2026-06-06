// Netlify Edge Function — Accept: text/markdown content negotiation
// Serves the clean .md twin of a page when a client explicitly prefers Markdown,
// HTML otherwise. Same URL, two representations (RFC 9110 content negotiation).
// Scoped to "/" and "/blogs/*" via netlify.toml.

interface AcceptEntry { type: string; q: number; }

function parseAccept(header: string): AcceptEntry[] {
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

function qualityFor(entries: AcceptEntry[], candidate: string): number {
  const [primary] = candidate.split("/");
  let bestSpec = -1, bestQ = 0;
  for (const { type, q } of entries) {
    const spec = type === candidate ? 3 : type === `${primary}/*` ? 2 : type === "*/*" ? 1 : -1;
    if (spec < 0) continue;
    if (spec > bestSpec || (spec === bestSpec && q > bestQ)) { bestSpec = spec; bestQ = q; }
  }
  return bestQ;
}

function hasExplicit(entries: AcceptEntry[], candidate: string): boolean {
  return entries.some((e) => e.type === candidate && e.q > 0);
}

export default async function (request: Request, context: { next: () => Promise<Response> }) {
  const url = new URL(request.url);
  const path = url.pathname;

  // Pass through .md twins and any file with an extension (assets handle themselves).
  if (path.endsWith(".md") || /\.[a-z0-9]+$/i.test(path)) {
    return context.next();
  }

  // Map a page URL to its Markdown twin.
  const mdPath = path === "/"
    ? "/index.md"
    : path.replace(/\/+$/, "") + ".md";
  const htmlLink = `<${path}>; rel="alternate"; type="text/html"`;
  const mdLink = `<${mdPath}>; rel="alternate"; type="text/markdown"`;

  const accept = parseAccept(request.headers.get("accept") ?? "");
  const mdQ = qualityFor(accept, "text/markdown");
  const htmlQ = qualityFor(accept, "text/html");

  // Neither representation is acceptable -> 406 (machine-readable refusal).
  if (mdQ === 0 && htmlQ === 0) {
    return new Response("Not Acceptable", {
      status: 406,
      headers: {
        "Content-Type": "text/plain; charset=utf-8",
        "Vary": "Accept",
        "Link": `${htmlLink}, ${mdLink}`,
      },
    });
  }

  // Client explicitly prefers Markdown (and ranks it >= HTML) -> serve the .md twin.
  if (hasExplicit(accept, "text/markdown") && mdQ >= htmlQ) {
    try {
      const mdResp = await fetch(new URL(mdPath, url.origin), { headers: { "Accept": "text/markdown" } });
      if (mdResp.ok) {
        return new Response(await mdResp.text(), {
          status: 200,
          headers: {
            "Content-Type": "text/markdown; charset=utf-8",
            "Vary": "Accept",
            "Link": htmlLink,
          },
        });
      }
    } catch (_) { /* fall through to HTML */ }
  }

  // Default: serve HTML, advertise the Markdown twin + mark Vary for caches.
  const res = await context.next();
  const out = new Response(res.body, res);
  out.headers.set("Vary", "Accept");
  out.headers.append("Link", mdLink);
  return out;
}
