from fastapi import FastAPI

app = FastAPI(title="Clearing House")

@app.get("/health")
def health():
    return {"status": "ok"}
