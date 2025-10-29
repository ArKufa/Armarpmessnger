import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Получаем URL базы данных из переменных окружения
DATABASE_URL = os.getenv('postgresql://arma_user:QRs0QZwsuSQjW2LX3pHfvMttLlYiuAbb@dpg-d418obili9vc739h7t8g-a/arma_messenger')

# Исправляем URL для SQLAlchemy (Render использует postgres://, а нужно postgresql://)
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

# Создаем движок базы данных
engine = create_engine(DATABASE_URL)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

# Функция для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
