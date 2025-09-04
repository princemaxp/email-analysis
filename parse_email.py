import email
import re
from bs4 import BeautifulSoup

def parse_email(file_path):
    with open(file_path, "rb") as f:
        msg = email.message_from_binary_file(f)

    headers = dict(msg.items())
    
    # Extract body (handle plain + HTML)
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body += part.get_payload(decode=True).decode(errors="ignore")
            elif part.get_content_type() == "text/html":
                html = part.get_payload(decode=True).decode(errors="ignore")
                soup = BeautifulSoup(html, "html.parser")
                body += soup.get_text()
    else:
        body = msg.get_payload(decode=True).decode(errors="ignore")

    # Extract URLs
    urls = re.findall(r'(https?://\S+)', body)

    return headers, body, urls
