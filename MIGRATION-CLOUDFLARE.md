# Migrating rawmktg.com from Netlify to Cloudflare Pages

The repo is now ready for Cloudflare Pages. The Netlify-specific config has been
ported to files Cloudflare reads natively:

| Netlify (old)                       | Cloudflare Pages (new)            |
|-------------------------------------|-----------------------------------|
| `netlify.toml` `[[redirects]]`      | `_redirects`                      |
| `netlify.toml` `[[headers]]`        | `_headers`                        |
| Edge function `md-negotiate`        | `functions/_middleware.js`        |
| `pretty_urls = true`                | native (Pages serves clean URLs)  |
| `not_found = "/404.html"`           | native (Pages serves `/404.html`) |

`netlify.toml` is left in place as a harmless fallback; Cloudflare ignores it.

---

## 1. Create the Pages project (5 min)

1. Cloudflare dashboard → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**.
2. Authorise GitHub and pick **`vinayakrawmktg/rawmktg`**, production branch **`main`**.
3. Build settings:
   - **Framework preset:** None
   - **Build command:** *(leave empty)*
   - **Build output directory:** `/`
   - **Root directory:** `/`

   Leaving the build command empty is the bulletproof option: every `.html`, `.md`,
   `sitemap.xml` and `llms*.txt` is already committed, so Pages just serves them.
   (Optional, later: set the build command to
   `pip install -r requirements.txt && python3 scripts/generate_llm_md.py`
   to regenerate the markdown twins on each deploy, once the site is confirmed up.)
4. **Save and Deploy.** You'll get a `https://rawmktg.pages.dev` URL. Open it and
   click around — every page, redirect and the `.md` twins should work there before
   you touch DNS.

## 2. Point the domain at Pages

- **Custom domains** tab → **Set up a custom domain** → add `rawmktg.com`, then `www.rawmktg.com`.
- If `rawmktg.com` already uses **Cloudflare nameservers**, Pages adds the DNS records for you in one click.
- If DNS is still at your registrar / on Netlify DNS, move the domain onto Cloudflare
  first (add the site in Cloudflare → update nameservers at the registrar), then add
  the custom domain. This nameserver change is the only slow step (can take a few hours).

## 3. www → apex redirect (Pages can't do host redirects in `_redirects`)

Cloudflare dashboard → **Rules** → **Redirect Rules** → **Create rule**:
- When incoming requests match: **Hostname** equals `www.rawmktg.com`
- Then: **Static** redirect to `https://rawmktg.com/${http.request.uri.path}` — Status **301**.

## 4. ⚠️ Newsletter form needs a new backend

The signup form (on ~39 pages) used **Netlify Forms** (`data-netlify="true"`,
action `/subscribed`). Cloudflare Pages has no built-in form handler, so submissions
will stop being captured after the move. Pick one:

- **Third-party (fastest):** point the form `action` at Formspree / Buttondown /
  ConvertKit / Mailchimp and drop the `data-netlify` attributes.
- **Cloudflare-native:** add a `functions/subscribed.js` Pages Function that handles
  the POST (store to KV / D1, or forward to an email provider's API).

The site is fully functional without this; only signup capture is affected. Say the
word and I'll wire either option across all pages.

## 5. Decommission Netlify

Once the Pages custom domain serves correctly and DNS has propagated, delete or
unpublish the Netlify site (or just leave it, detached from DNS) so there's one source
of truth.

---

### Notes
- **Clean URLs:** Pages serves `/blogs/foo.html` at `/blogs/foo` automatically, matching every `rel="canonical"`.
- **IndexNow:** the old build pinged IndexNow on deploy. With an empty build command that won't run; run `python3 scripts/indexnow_submit.py` manually after a content push, or add it back to the build command later.
- **`functions/_middleware.js`** is fail-open: any error just serves normal HTML, so it can't take the site down. Delete the `functions/` folder to disable markdown negotiation entirely (the `.md` files stay reachable directly).
