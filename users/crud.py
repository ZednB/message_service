from typing import List
from fastapi.responses import RedirectResponse

from fastapi import APIRouter, Form, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import User as DbUser
from db import get_db
from users.models import User as User
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi_users import FastAPIUsers

router = APIRouter(
    prefix='/user',
    tags=['user'],
)
templates = Jinja2Templates(directory="templates")

fastapi_users = FastAPIUsers[User, int](
    get_db,
    [],
)


@router.get("/create", response_class=HTMLResponse)
async def get_create_user_form(request: Request):
    return templates.TemplateResponse("users/users_create.html", {"request": request})


@router.post("/create", response_model=DbUser)
# Регистрация нового пользователя
async def create_user(
        name: str = Form(...),
        email: str = Form(...),
        age: int = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    # Проверка, существует ли пользователь с таким email
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    # Создание SQLAlchemy объекта
    db_user = User(name=name, email=email, age=age, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Преобразование SQLAlchemy объекта в Pydantic
    return RedirectResponse(url="/user/list", status_code=303)


@router.get("/login", response_class=HTMLResponse)
def login_user_form(request: Request):
    return templates.TemplateResponse("users/user_login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse)
# Авторизация пользователя
async def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.email == email, User.password == password).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Неверный логин или пароль")

    response = RedirectResponse(url="/user/list", status_code=303)
    response.set_cookie(key="current_user_id", value=str(db_user.id), httponly=True)
    return response


def get_current_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/list", response_class=HTMLResponse)
async def get_list_form(
    request: Request,
    db: Session = Depends(get_db)
):
    user_id = request.cookies.get("current_user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Неавторизованный доступ")

    current_user = db.query(User).filter(User.id == int(user_id)).first()
    if not current_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    db_user = db.query(User).all()
    return templates.TemplateResponse(
        "users/users_list.html",
        {"request": request, "db_user": db_user, "user_id": current_user.id}
    )


@router.get("/list", response_model=List[DbUser])
async def list_user(
        request: Request,
        db: Session = Depends(get_db)
):
    # Получаем ID текущего пользователя из куков
    user_id = request.cookies.get("current_user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Неавторизованный доступ")

    # Проверяем существование текущего пользователя в базе
    current_user = db.query(User).filter(User.id == int(user_id)).first()
    if not current_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Возвращаем список всех пользователей
    return db.query(User).all()


@router.get("/profile/{user_id}", response_class=HTMLResponse)
async def get_profile(user_id: int, request: Request, db: Session = Depends(get_db)):
    current_user_id = request.cookies.get("current_user_id")
    if not current_user_id:
        raise HTTPException(status_code=401, detail="Неавторизованный доступ")

    current_user = db.query(User).filter(User.id == int(current_user_id)).first()
    if not current_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return templates.TemplateResponse("users/user_profile.html", {"request": request, "current_user": current_user, "user": user})