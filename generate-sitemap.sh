#!/bin/bash
# Run this from the repo root before every push to keep sitemap.xml and feed.xml current.
# Usage: bash generate-sitemap.sh

SITE="https://rawmktg.com"
TODAY=$(date +%Y-%m-%d)
OUT="sitemap.xml"

cat > "$OUT" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>${SITE}/</loc>
    <lastmod>${TODAY}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
EOF

for f in Blogs/*.html; do
  slug=$(basename "$f")
  cat >> "$OUT" <<EOF
  <url>
    <loc>${SITE}/Blogs/${slug}</loc>
    <lastmod>${TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
EOF
done

echo "</urlset>" >> "$OUT"
echo "sitemap.xml updated with $(ls Blogs/*.html | wc -l | tr -d ' ') articles."

# ── Regenerate feed.xml ──────────────────────────────────────────────────────
FEED="feed.xml"
BUILD_DATE=$(date -u "+%a, %d %b %Y 00:00:00 +0000")

cat > "$FEED" <<FEEDEOF
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>rawmktg.</title>
    <link>https://rawmktg.com</link>
    <description>B2B marketing intelligence for the AI era -- SEO, GEO, and AI search visibility for SaaS companies.</description>
    <language>en-us</language>
    <copyright>rawmktg.</copyright>
    <atom:link href="https://rawmktg.com/feed.xml" rel="self" type="application/rss+xml" />
    <lastBuildDate>${BUILD_DATE}</lastBuildDate>
FEEDEOF

# Sort by article:published_time descending, then emit items
for f in $(grep -rl 'article:published_time' Blogs/*.html | xargs grep -l ''); do
  pub=$(grep -oP '(?<=article:published_time" content=")[^"]+' "$f" | head -1)
  echo "$pub $f"
done | sort -r | while read -r pubiso filepath; do
  slug=$(basename "$filepath")
  title=$(grep -oP '(?<=<title>)[^<]+' "$filepath" | head -1)
  desc=$(grep -oP '(?<=name="description" content=")[^"]+' "$filepath" | head -1)
  # Convert ISO date to RFC 2822
  rfc_date=$(date -u -d "${pubiso}" "+%a, %d %b %Y 00:00:00 +0000" 2>/dev/null || date -u -jf "%Y-%m-%dT%H:%M:%SZ" "${pubiso}" "+%a, %d %b %Y 00:00:00 +0000")
  cat >> "$FEED" <<ITEMEOF

    <item>
      <title><![CDATA[${title}]]></title>
      <link>${SITE}/Blogs/${slug}</link>
      <guid isPermaLink="true">${SITE}/Blogs/${slug}</guid>
      <pubDate>${rfc_date}</pubDate>
      <description><![CDATA[${desc}]]></description>
    </item>
ITEMEOF
done

cat >> "$FEED" <<FEEDEOF

  </channel>
</rss>
FEEDEOF

echo "feed.xml regenerated."

# ── Ping IndexNow ────────────────────────────────────────────────────────────
INDEXNOW_KEY="cb521429cad14c589e4fb6616e114002"

# Build JSON URL list from sitemap
URL_LIST="\"${SITE}/\""
for f in Blogs/*.html; do
  slug=$(basename "$f")
  URL_LIST="${URL_LIST}, \"${SITE}/Blogs/${slug}\""
done

PAYLOAD=$(cat <<JSON
{
  "host": "rawmktg.com",
  "key": "${INDEXNOW_KEY}",
  "keyLocation": "https://rawmktg.com/${INDEXNOW_KEY}.txt",
  "urlList": [${URL_LIST}]
}
JSON
)

HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  -X POST "https://api.indexnow.org/indexnow" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "${PAYLOAD}")

if [ "$HTTP_STATUS" = "200" ] || [ "$HTTP_STATUS" = "202" ]; then
  echo "IndexNow pinged successfully (HTTP ${HTTP_STATUS}) -- $(ls Blogs/*.html | wc -l | tr -d ' ') URLs submitted."
else
  echo "IndexNow ping returned HTTP ${HTTP_STATUS} -- check manually."
fi
