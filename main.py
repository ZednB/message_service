from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
import db
from chat.routers import router as router_chat
from users.crud import router as router_user
from users.models import User

app = FastAPI()
app.include_router(router_chat)
app.include_router(router_user)
templates = Jinja2Templates(directory="templates")


@app.get('/')
async def get_main_page(request: Request):
    return templates.TemplateResponse("chat/base.html", {"request": request})


@app.get('/{user_id}/{recipient_id}')
async def get_chat_page(request: Request, user_id: int, recipient_id: int, db: Session = Depends(db.get_db)):
        user = db.query(User).filter(User.id == user_id).first()
        recipient = db.query(User).filter(User.id == recipient_id).first()
        if user is None or recipient is None:
            return HTMLResponse(content="Пользователь не найден", status_code=404)
        return templates.TemplateResponse("chat/chat.html",{
            "request": request,
            "user_id": user_id,
            "recipient_id": recipient_id,
            "username": user.name
        })
