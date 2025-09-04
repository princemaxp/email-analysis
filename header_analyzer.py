def analyze_headers(headers):
    findings = []

    # Check if SPF/DKIM/DMARC are missing
    auth_results = headers.get("Authentication-Results", "").lower()
    if "spf=fail" in auth_results:
        findings.append("Header: SPF check failed")
    if "dkim=fail" in auth_results:
        findings.append("Header: DKIM check failed")
    if "dmarc=fail" in auth_results:
        findings.append("Header: DMARC check failed")

    # Check suspicious "From" vs "Reply-To"
    from_addr = headers.get("From", "")
    reply_to = headers.get("Reply-To", "")
    if reply_to and reply_to not in from_addr:
        findings.append(f"Header: Mismatch between From and Reply-To ({reply_to})")

    return findings
