from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
# from models import User # Will be needed later

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
@router.get("/home")
async def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/dashboard")
async def DashBoard(request: Request, db: Session = Depends(get_db)):
    # Mocking data for now as in the original project
    latitude, longitude = 0.0, 0.0 
    total_bins, half_filled_bins, empty_bins = 20, 10, 20
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "latitude": latitude,
        "longitude": longitude,
        "total_bins": total_bins,
        "half_filled_bins": half_filled_bins,
        "empty_bins": empty_bins
    })

@router.get("/about")
async def About_page(request: Request):
    return templates.TemplateResponse("About.html", {"request": request})

@router.get("/disease_monitor")
@router.get("/main index.html")
async def disease_monitor(request: Request):
    return templates.TemplateResponse("main_index.html", {"request": request})

@router.get("/monitor_dashboard")
@router.get("/monitor_dashboard.html")
async def monitor_dashboard(request: Request):
    return templates.TemplateResponse("monitor_dashboard.html", {"request": request})

@router.get("/grade")
@router.get("/grade.html")
async def grade(request: Request):
    return templates.TemplateResponse("grade.html", {"request": request})

@router.get("/marketplace")
@router.get("/Marketplace_dashboard.html")
async def marketplace(request: Request):
    return templates.TemplateResponse("marketplace_dashboard.html", {"request": request})

@router.get("/predictions")
@router.get("/predictions.html")
async def predictions(request: Request):
    return templates.TemplateResponse("predictions.html", {"request": request})

@router.get("/history")
@router.get("/history.html")
async def history(request: Request):
    return templates.TemplateResponse("history.html", {"request": request})

@router.get("/what_to_grow")
@router.get("/what_to_grow.html")
async def what_to_grow(request: Request):
    return templates.TemplateResponse("what_to_grow.html", {"request": request})

@router.get("/chatbot")
@router.get("/Chat Bot.html")
async def chatbot(request: Request):
    return templates.TemplateResponse("Chat Bot.html", {"request": request})

@router.get("/gemini_info")
@router.get("/index for gemini.html")
async def gemini_info(request: Request):
    return templates.TemplateResponse("index for gemini.html", {"request": request})

@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "form": {}}) # form mock for template compat

@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "form": {}}) # form mock for template compat
