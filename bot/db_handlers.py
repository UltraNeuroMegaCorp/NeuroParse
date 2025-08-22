from sqlalchemy.orm import Session
import json


class DbHandler:
    def __init__(self, db: Session, model):
        self.db = db
        self.model = model

    def add_message(self, chat_title, username,
                    message_text, message_time,
                    reply_to_user_username=None, reply_to_text=None):

        tmp = {
            "chat_title": chat_title,
            "username": username,
            "message_text": message_text,
            "message_time": message_time.isoformat(),
            "reply_to_user_username": reply_to_user_username,
            "reply_to_text": reply_to_text,
        }

        full_message_json = json.dumps(tmp, ensure_ascii=False)
        print(full_message_json)

        msg = self.model(
            chat_title=chat_title,
            username=username,
            message_text=message_text,
            message_time=message_time,
            reply_to_user_username=reply_to_user_username,
            reply_to_text=reply_to_text,
            raw_json=full_message_json,
        )
        self.db.add(msg)
        self.db.commit()
        self.db.refresh(msg)
        return msg

    def get_all(self):
        return self.db.query(self.model).all()
