from fastapi import FastAPI, File, UploadFile
import analyze_email_main   # <-- updated import

app = FastAPI()

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    content = await file.read()
    with open("temp.eml", "wb") as f:
        f.write(content)

    results = analyze_email_main.analyze("temp.eml")
    return {"results": results}
