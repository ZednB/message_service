from sqlalchemy.orm import Session

from chat.models import Message


def save_message(db: Session, sender_id: int, recipient_id: int, content: str):
    message = Message(sender_id=sender_id, recipient_id=recipient_id, content=content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message
