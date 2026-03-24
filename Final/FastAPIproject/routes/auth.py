from fastapi import APIRouter, Depends, HTTPException, status, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserLogin
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    email_address: str = Form(...),
    password1: str = Form(...),
    password2: str = Form(...),
    db: Session = Depends(get_db)
):
    if password1 != password2:
        # In a real app, flash a message. Here we redirect with error or just 400.
        return templates.TemplateResponse("register.html", {"request": request, "error": "Passwords do not match"})
    
    existing_user = db.query(User).filter((User.username == username) | (User.email_address == email_address)).first()
    if existing_user:
         return templates.TemplateResponse("register.html", {"request": request, "error": "Username or Email already exists"})

    new_user = User(username=username, email_address=email_address, password_hash=password1)
    db.add(new_user)
    db.commit()
    
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    # Note: Sessions would need a middleware. For now, simple redirect.
    return response

@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if user and user.check_password_correction(password):
        response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
        # Set a session cookie or similar here
        return response
    
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid username or password"})

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/login")
    # Clear session cookie here
    return response
