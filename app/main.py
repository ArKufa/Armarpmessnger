from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import crud, models, database, bot
import json

app = FastAPI()

# CORS для связи с React фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # На продакшене укажите точный URL вашего фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем базу данных
models.Base.metadata.create_all(bind=database.engine)

# Менеджер WebSocket соединений
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                self.active_connections.remove(connection)

manager = ConnectionManager()

# API для получения списка персонажей
@app.get("/characters/")
def read_characters(db: Session = Depends(database.get_db)):
    characters = crud.get_characters(db)
    return characters

# API для получения сообщений
@app.get("/messages/")
def read_messages(db: Session = Depends(database.get_db)):
    messages = crud.get_messages(db)
    return messages

# WebSocket для отправки новых сообщений из веб-интерфейса
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Сохраняем сообщение в БД
            db = database.SessionLocal()
            try:
                crud.create_message(db, message_data["character_name"], message_data["content"])
                # Отправляем сообщение в Discord канал (#messenger-logs)
                await bot.send_message_to_discord(YOUR_DISCORD_CHANNEL_ID, message_data["character_name"], message_data["content"])
                # Рассылаем обновление всем подключенным клиентам
                await manager.broadcast(json.dumps(message_data))
            finally:
                db.close()
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
