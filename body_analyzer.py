import requests

HF_API_URL = "https://api-inference.huggingface.co/models/mrm8488/bert-tiny-finetuned-sms-spam-detection"
HF_HEADERS = {"Authorization": "Bearer YOUR_HF_API_KEY"}  # Free account

def analyze_body(text):
    response = requests.post(HF_API_URL, headers=HF_HEADERS, json={"inputs": text[:1000]})
    result = response.json()
    
    if isinstance(result, list) and result:
        label = result[0]['label']
        score = result[0]['score']
        return [f"Body: {label} (confidence {score:.2f})"]
    return ["Body: Analysis failed or inconclusive"]
