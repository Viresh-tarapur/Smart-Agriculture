from fastapi import APIRouter, Depends, HTTPException, status, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
from models import User
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/login")
async def login_page(request: Request):
    if request.cookies.get("username"):
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse(request=request, name="login.html", context={})

@router.get("/register")
async def register_page(request: Request):
    if request.cookies.get("username"):
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse(request=request, name="register.html", context={})

@router.get("/profile")
async def profile_page(request: Request, db: Session = Depends(get_db)):
    username = request.cookies.get("username")
    if not username:
        return RedirectResponse(url="/login", status_code=302)
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse(request=request, name="profile.html", context={
        "username": user.username,
        "email": user.email_address,
        "user_id": user.id
    })

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
    
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="username", value=username, max_age=86400)
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
        response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="username", value=username, max_age=86400)
        return response
    
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid username or password"})

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/login")
    # Clear session cookie here
    return response
