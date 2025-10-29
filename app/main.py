from fastapi import FastAPI, Request, WebSocket, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from . import database, models, crud
import os

# Сначала создаем app
app = FastAPI()

# Затем настраиваем статические файлы и шаблоны
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Создаем таблицы при старте
@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=database.engine)

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request, db: Session = Depends(database.get_db)):
    characters = crud.get_characters(db)
    messages = crud.get_messages(db)
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "characters": characters,
        "messages": messages
    })

@app.post("/send_message/")
async def send_message(
    character_name: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(database.get_db)
):
    # Сохраняем сообщение в БД
    crud.create_message(db, character_name, content)
    # Здесь будет отправка в Discord (добавим позже)
    return RedirectResponse("/", status_code=303)

@app.get("/health")
async def health():
    return {"status": "ok"}

# WebSocket для реального времени (опционально)
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message: {data}")
