from sqlalchemy.orm import Session

from chat.models import Message


def get_message_history(db: Session, user_id: int, recipient_id: int, limit: int = 50):
    return db.query(Message).filter(
        ((Message.sender_id == user_id) & (Message.recipient_id == recipient_id)) |
        ((Message.sender_id == recipient_id) & (Message.recipient_id == user_id))
    ).order_by(Message.timestamp.desc()).limit(limit).all()
