from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import MESSAGE_DB_PATH, LISTENER_DB_PATH

engineMessage = create_engine(MESSAGE_DB_PATH, echo=False, future=True)
engineListener = create_engine(LISTENER_DB_PATH, echo=False, future=True)

SessionLocalMessage = sessionmaker(bind=engineMessage, autoflush=False, autocommit=False, future=True)
SessionLocalListener = sessionmaker(bind=engineListener, autoflush=False, autocommit=False, future=True)

BaseMessage = declarative_base()
BaseListener = declarative_base()


def get_db_message():
    db = SessionLocalMessage()
    try:
        yield db
    finally:
        db.close()


def get_db_listener():
    db = SessionLocalListener()
    try:
        yield db
    finally:
        db.close()


def init_db():
    BaseMessage.metadata.create_all(bind=engineMessage)
    BaseListener.metadata.create_all(bind=engineListener)
