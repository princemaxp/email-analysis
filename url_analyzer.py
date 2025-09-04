import requests

def analyze_urls(urls):
    findings = []
    for url in urls:
        try:
            res = requests.get(f"https://checkurl.phishtank.com/checkurl/{url}?format=json")
            data = res.json()
            if data.get("results", {}).get("valid") and data["results"].get("in_database"):
                findings.append(f"URL: {url} is reported as phishing (PhishTank)")
            else:
                findings.append(f"URL: {url} not flagged (PhishTank)")
        except:
            findings.append(f"URL: {url} could not be checked")
    return findings
