from fastapi import FastAPI, Request, WebSocket, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse

# Добавьте в начало после создания app
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Замените или добавьте эти роуты
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
    # Отправляем в Discord
    await bot.send_message_to_discord(YOUR_DISCORD_CHANNEL_ID, character_name, content)
    return RedirectResponse("/", status_code=303)
