from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from db import BaseListener, BaseMessage
from datetime import datetime


class Message(BaseMessage):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_title = Column(String(255))
    username = Column(String(255))
    message_text = Column(Text)
    message_time = Column(DateTime, default=datetime.utcnow)
    reply_to_user_username = Column(Integer, nullable=True)
    reply_to_text = Column(Text, nullable=True)
    raw_json = Column(JSON)

    def __repr__(self):
        return f"<Message {self.id} {self.username}: {self.message_text[:20]}>"


class Listener(BaseListener):
    __tablename__ = "listener"

    id = Column(Integer, primary_key=True, index=True)
    chat_title = Column(String(255))
    username = Column(String(255))
    message_text = Column(Text)
    message_time = Column(DateTime, default=datetime.utcnow)
    reply_to_user_username = Column(Integer, nullable=True)
    reply_to_text = Column(Text, nullable=True)
    raw_json = Column(JSON)

    def __repr__(self):
        return f"<Message {self.id} {self.username}: {self.message_text[:20]}>"
