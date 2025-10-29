from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "ARMA RP Messenger API is working!"}

@app.get("/health")
async def health():
    return {"status": "ok"}

# Временный эндпоинт для тестирования
@app.get("/test")
async def test():
    return {"test": "success", "python_version": "3.13"}
