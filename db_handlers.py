from sqlalchemy.orm import Session
from models import Message


class DbHandler:
    def __init__(self, db: Session):
        self.db = db

    def add_message(self, chat_title, username,
                    message_text, message_time,
                    reply_to_user_username=None, reply_to_text=None):
        msg = Message(
            chat_title=chat_title,
            username=username,
            message_text=message_text,
            message_time=message_time,
            reply_to_user_username=reply_to_user_username,
            reply_to_text=reply_to_text
        )
        self.db.add(msg)
        self.db.commit()
        self.db.refresh(msg)
        return msg

    def get_all(self):
        return self.db.query(Message).all()

    def get_by_user(self, user_id: int):
        return self.db.query(Message).filter(Message.user_id == user_id).all()

    def get_chat_messages(self, chat_id: int):
        return self.db.query(Message).filter(Message.chat_id == chat_id).all()
