import requests
import os

HF_API_KEY = os.getenv("HF_API_KEY")  # Hugging Face free account
HF_HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

MODELS = {
    "ai_detector": "roberta-base-openai-detector",
    "sentiment": "finiteautomata/bertweet-base-sentiment-analysis",
    "spam": "mrm8488/bert-tiny-finetuned-sms-spam-detection",
}

def query_hf(model, text):
    url = f"https://api-inference.huggingface.co/models/{model}"
    res = requests.post(url, headers=HF_HEADERS, json={"inputs": text[:1000]})
    return res.json()

def analyze_body(text):
    findings = []

    # 1. AI-generated detection
    try:
        result = query_hf(MODELS["ai_detector"], text)
        if isinstance(result, list):
            findings.append(f"Body: AI Detector → {result[0]['label']} (confidence {result[0]['score']:.2f})")
    except:
        findings.append("Body: AI detection failed")

    # 2. Sentiment / Tone
    try:
        result = query_hf(MODELS["sentiment"], text)
        if isinstance(result, list):
            findings.append(f"Body: Sentiment → {result[0]['label']} (confidence {result[0]['score']:.2f})")
    except:
        findings.append("Body: Sentiment analysis failed")

    # 3. Spam vs Ham
    try:
        result = query_hf(MODELS["spam"], text)
        if isinstance(result, list):
            findings.append(f"Body: Spam Detector → {result[0]['label']} (confidence {result[0]['score']:.2f})")
    except:
        findings.append("Body: Spam detection failed")

    return findings
