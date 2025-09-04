from parse_email import parse_email
from header_analyzer import analyze_headers
from body_analyzer import analyze_body
from url_analyzer import analyze_urls

def analyze(file_path):
    headers, body, urls = parse_email(file_path)

    results = []
    results.extend(analyze_headers(headers))
    results.extend(analyze_body(body))
    results.extend(analyze_urls(urls))

    if not results:
        return ["No issues detected. Email looks safe."]
    return results

if __name__ == "__main__":
    file_path = "sample.eml"
    findings = analyze(file_path)
    for f in findings:
        print(f)
