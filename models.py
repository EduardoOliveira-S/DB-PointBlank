from sqlalchemy import Column, Integer, String
from database import Base

class Account(Base):
    __tablename__ = "accounts"

    player_id = Column(Integer, primary_key=True, index=True)
    login = Column(String)
    password = Column(String)
    rank = Column(Integer)
