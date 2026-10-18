import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(64), unique=True, index=True, nullable=False)
    link_type = Column(String(16), default="prank") # "prank" ou "date"
    
    # Customizações
    question = Column(String(255), nullable=True)
    target_name = Column(String(100), nullable=True) # Nome da garota/amigo
    creator_name = Column(String(100), nullable=True) # Nome do autor
    
    # Canais de notificação do autor
    creator_whatsapp = Column(String(50), nullable=True)
    creator_callmebot_key = Column(String(100), nullable=True) # Chave do robô WhatsApp
    creator_facebook = Column(String(100), nullable=True)
    creator_line = Column(String(100), nullable=True) # LINE ID ou link de contato
    creator_webhook = Column(String(255), nullable=True)
    
    # Disponibilidade do convidante (JSON com timezone, duration_min, days e taken)
    google_credentials = Column(Text, nullable=True) # Obsoleto (mantido para compatibilidade com banco SQLite existente)
    available_days = Column(Text, nullable=True) # JSON: {"timezone": "...", "duration_min": 180, "days": [{"date": "YYYY-MM-DD", "times": ["HH:MM"]}], "taken": ["YYYY-MM-DD|HH:MM"]}
    
    # Estatísticas
    views = Column(Integer, default=0)
    total_dodges = Column(Integer, default=0)
    accepted = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    responses = relationship("DateResponse", back_populates="link", cascade="all, delete-orphan")

class DateResponse(Base):
    __tablename__ = "date_responses"

    id = Column(Integer, primary_key=True, index=True)
    link_id = Column(Integer, ForeignKey("links.id"), nullable=False)
    
    selected_date = Column(String(32), nullable=True) # ex: "2026-10-25"
    selected_time = Column(String(32), nullable=True) # ex: "20:00"
    dodge_count = Column(Integer, default=0)
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    link = relationship("Link", back_populates="responses")
