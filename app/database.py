import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Для Render.com
DATABASE_URL = os.getenv("postgresql://arma_user:QRs0QZwsuSQjW2LX3pHfvMttLlYiuAbb@dpg-d418obili9vc739h7t8g-a/arma_messenger")

# Важно: исправляем URL для SQLAlchemy
if DATABASE_URL and DATABASE_URL.startswith("postgresql://arma_user:QRs0QZwsuSQjW2LX3pHfvMttLlYiuAbb@dpg-d418obili9vc739h7t8g-a/arma_messenger"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://arma_user:QRs0QZwsuSQjW2LX3pHfvMttLlYiuAbb@dpg-d418obili9vc739h7t8g-a/arma_messenger", "postgresql://arma_user:QRs0QZwsuSQjW2LX3pHfvMttLlYiuAbb@dpg-d418obili9vc739h7t8g-a/arma_messenger", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
