import discord
from discord.ext import commands
import os
from sqlalchemy.orm import Session
from . import crud, models, database

# Настройка интентов
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Бот {bot.user} подключился к Discord!')

# Обработчик для сбора квент из канала #character-profiles
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Игнорируем сообщения не из нужных каналов
    if message.channel.name not in ["character-profiles", "rp-chat"]:
        return

    # Сохраняем квенту в БД
    if message.channel.name == "character-profiles":
        # Простой парсинг. Можно улучшить, например, использовать Markdown или эмбеды.
        lines = message.content.split('\n')
        char_name = lines[0] if lines else "Unknown"
        char_bio = '\n'.join(lines[1:]) if len(lines) > 1 else ""

        db: Session = database.SessionLocal()
        try:
            crud.create_character(db, message.author.id, message.id, char_name, char_bio)
            print(f"Создан персонаж: {char_name}")
        except Exception as e:
            print(f"Ошибка при сохранении персонажа: {e}")
        finally:
            db.close()

    # Пересылаем сообщения из RP чата в веб-мессенджер
    elif message.channel.name == "rp-chat":
        db: Session = database.SessionLocal()
        try:
            # Ищем автора сообщения в нашей базе персонажей
            character = crud.get_character_by_discord_id(db, message.author.id)
            if character:
                crud.create_message(db, character.name, message.content, message.id)
                print(f"Сообщение от {character.name} сохранено: {message.content}")
        except Exception as e:
            print(f"Ошибка при сохранении сообщения: {e}")
        finally:
            db.close()

    await bot.process_commands(message)

# Функция для отправки сообщения из мессенджера обратно в Discord
async def send_message_to_discord(channel_id: int, character_name: str, content: str):
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(f"**{character_name}:** {content}")
