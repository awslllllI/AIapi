"""Interactively create a Playwright storage state for an explicitly authorized site.

Run only for sites that permit this form of browser automation. This utility
does not solve or bypass CAPTCHA/MFA; the user completes any normal challenge.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a browser session state for one authorized site.")
    parser.add_argument("--site-id", required=True)
    parser.add_argument("--config", default="gateway/browser-sites.json")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.is_file():
        parser.error(f"site config not found: {config_path}")
    try:
        document = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        parser.error(f"cannot read site config: {exc}")

    site = next(
        (item for item in document.get("sites", []) if isinstance(item, dict) and item.get("id") == args.site_id),
        None,
    )
    if site is None:
        parser.error(f"unknown site id: {args.site_id}")
    if not site.get("enabled", False) or not site.get("automation_authorized", False):
        parser.error("site must explicitly set enabled=true and automation_authorized=true")
    url = str(site.get("base_url") or "")
    allowed = {str(host).lower() for host in site.get("allowed_domains", [])}
    parsed = urlparse(url)
    if not parsed.hostname or parsed.hostname.lower() not in allowed:
        parser.error("base_url host must be included in allowed_domains")
    if parsed.scheme != "https" and parsed.hostname not in ("127.0.0.1", "localhost"):
        parser.error("non-local sites must use HTTPS")

    auth = site.get("auth") if isinstance(site.get("auth"), dict) else {}
    state_path = Path(auth.get("storage_state_path") or f".local/browser-sessions/{args.site_id}.json")
    state_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded")
        print(f"Opened {url}")
        print("Complete the site's normal sign-in manually in the browser window.")
        print("Do not proceed if the site's rules prohibit browser automation.")
        print("Do not attempt to bypass CAPTCHA, MFA, access controls, or automation restrictions.")
        input("When the authorized session is ready, return here and press Enter to save it (Ctrl+C to cancel): ")
        current_host = (urlparse(page.url).hostname or "").lower()
        if current_host not in allowed:
            browser.close()
            raise SystemExit(f"Refusing to save session: current host {current_host!r} is outside allowed_domains")
        context.storage_state(path=str(state_path))
        browser.close()

    print(f"Saved browser session state to {state_path}")
    print("Treat this file as a secret. It is ignored by Git and must not be shared.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
