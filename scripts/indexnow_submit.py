#!/usr/bin/env python3
"""Build step: submit all sitemap URLs to IndexNow so Bing and Yandex are pinged to
crawl on every deploy. Uses the key already served at the site root. Non-fatal: any
failure prints a notice and exits 0 so it can never break a deploy."""
import os, re, json, sys, urllib.request

HOST = "rawmktg.com"
KEY = "cb521429cad14c589e4fb6616e114002"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
ENDPOINT = "https://api.indexnow.org/indexnow"

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sm = os.path.join(root, "sitemap.xml")
    if not os.path.exists(sm):
        print("[indexnow] no sitemap.xml found, skipping"); return
    urls = [u.strip() for u in re.findall(r"<loc>(.*?)</loc>", open(sm, encoding="utf-8").read()) if u.strip()]
    if not urls:
        print("[indexnow] no URLs in sitemap, skipping"); return
    payload = json.dumps({"host": HOST, "key": KEY, "keyLocation": KEY_LOCATION,
                          "urlList": urls}).encode("utf-8")
    req = urllib.request.Request(ENDPOINT, data=payload, method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            print(f"[indexnow] submitted {len(urls)} URLs -> HTTP {r.status}")
    except Exception as e:
        print(f"[indexnow] submit failed (non-fatal): {e}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("[indexnow] error (non-fatal):", e)
    sys.exit(0)
