#!/usr/bin/env python3
"""php-eol-check: see which PHP version a website exposes and whether it still gets security fixes.

No dependencies. Reads the X-Powered-By header (many hosts hide it; then the version is unknown)
and compares it with the active releases published by php.net.
Usage:
    python3 php_eol_check.py https://example.nl
    python3 php_eol_check.py example.nl --json

Made by Joepify (https://www.joepify.nl), MIT licence.
"""
import argparse, json, re, sys, urllib.request

# Security support end dates per branch, from https://www.php.net/supported-versions.php (checked 22 Oct 2026).
SECURITY_UNTIL = {"8.2": "2026-12-31", "8.3": "2027-12-31", "8.4": "2028-12-31", "8.5": "2029-12-31"}
UA = {"User-Agent": "php-eol-check/1.0 (+https://github.com/Joepify/php-eol-check)"}


def latest_releases():
    """Latest patch version per active branch, from php.net."""
    try:
        req = urllib.request.Request("https://www.php.net/releases/active.php", headers=UA)
        data = json.load(urllib.request.urlopen(req, timeout=15))
    except Exception:
        return {}
    out = {}
    for major in data.values():
        for branch, info in major.items():
            v = info.get("version")
            if v:
                out[branch] = v
    return out


def exposed_version(url):
    if not url.startswith("http"):
        url = "https://" + url
    req = urllib.request.Request(url, headers=UA, method="GET")
    with urllib.request.urlopen(req, timeout=20) as r:
        powered = r.headers.get("X-Powered-By", "") or ""
    m = re.search(r"PHP/(\d+)\.(\d+)\.(\d+)", powered)
    return url, powered, (f"{m.group(1)}.{m.group(2)}.{m.group(3)}" if m else None)


def verdict(version, latest):
    if not version:
        return "unknown", "The site does not expose its PHP version (good practice). Ask your host which version runs."
    branch = ".".join(version.split(".")[:2])
    tup = tuple(int(x) for x in version.split("."))
    if branch not in SECURITY_UNTIL:
        if tup < (8, 2, 0):
            return "end-of-life", f"PHP {branch} no longer receives security updates. Upgrade to 8.3 or newer."
        return "unknown-branch", f"PHP {branch} is not in the known support table."
    msg = f"PHP {branch} receives security fixes until {SECURITY_UNTIL[branch]}."
    lv = latest.get(branch)
    if lv and tuple(int(x) for x in lv.split(".")) > tup:
        return "outdated-patch", msg + f" Latest patch is {lv}; this site runs {version}. Update to get the latest security fixes."
    return "supported", msg


def main():
    ap = argparse.ArgumentParser(description="Check the PHP version a website exposes.")
    ap.add_argument("url")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    url, powered, version = exposed_version(a.url)
    latest = latest_releases()
    status, note = verdict(version, latest)
    out = {"url": url, "x_powered_by": powered or None, "php_version": version, "status": status, "note": note, "latest_per_branch": latest}
    if a.json:
        print(json.dumps(out, indent=2))
    else:
        print(f"URL: {url}\nX-Powered-By: {powered or '(not sent)'}\nPHP version: {version or 'unknown'}\nStatus: {status}\n{note}")
        print("\nWordPress? Read: https://www.joepify.nl/kennisbank/php-versie-wordpress")


if __name__ == "__main__":
    sys.exit(main())
