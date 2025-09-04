import requests
import os

# You can store API keys as environment variables
SAFE_BROWSING_API_KEY = os.getenv("SAFE_BROWSING_API_KEY")

def analyze_urls(urls):
    findings = []

    for url in urls:
        # --- 1. PhishTank ---
        try:
            res = requests.get(f"https://checkurl.phishtank.com/checkurl/{url}?format=json")
            data = res.json()
            if data.get("results", {}).get("in_database"):
                findings.append(f"URL: {url} is flagged as phishing (PhishTank)")
            else:
                findings.append(f"URL: {url} not flagged (PhishTank)")
        except:
            findings.append(f"URL: {url} could not be checked (PhishTank)")

        # --- 2. URLHaus ---
        try:
            res = requests.post("https://urlhaus-api.abuse.ch/v1/url/", data={"url": url})
            data = res.json()
            if data.get("query_status") == "ok":
                findings.append(f"URL: {url} is flagged as {data['url_status']} (URLHaus)")
            else:
                findings.append(f"URL: {url} not found in URLHaus")
        except:
            findings.append(f"URL: {url} could not be checked (URLHaus)")

        # --- 3. Google Safe Browsing ---
        if SAFE_BROWSING_API_KEY:
            try:
                payload = {
                    "client": {"clientId": "email-analysis-tool", "clientVersion": "1.0"},
                    "threatInfo": {
                        "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
                        "platformTypes": ["ANY_PLATFORM"],
                        "threatEntryTypes": ["URL"],
                        "threatEntries": [{"url": url}],
                    },
                }
                res = requests.post(
                    f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={SAFE_BROWSING_API_KEY}",
                    json=payload,
                )
                data = res.json()
                if "matches" in data:
                    findings.append(f"URL: {url} flagged by Google Safe Browsing")
                else:
                    findings.append(f"URL: {url} not flagged (Google Safe Browsing)")
            except:
                findings.append(f"URL: {url} could not be checked (Google Safe Browsing)")

    return findings
