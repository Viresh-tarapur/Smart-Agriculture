from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from chatgpt_service import get_crop_growing_info
import datetime

# from models import User # Will be needed later

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
@router.get("/home")
async def home_page(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})

@router.get("/dashboard")
async def DashBoard(request: Request, db: Session = Depends(get_db)):
    # Mocking data for now as in the original project
    latitude, longitude = 0.0, 0.0 
    total_bins, half_filled_bins, empty_bins = 20, 10, 20
    return templates.TemplateResponse(
        request=request, name="dashboard.html", context={
            "latitude": latitude,
            "longitude": longitude,
            "total_bins": total_bins,
            "half_filled_bins": half_filled_bins,
            "empty_bins": empty_bins
        }
    )

@router.get("/about")
async def About_page(request: Request):
    return templates.TemplateResponse(request=request, name="About.html", context={})

@router.get("/disease_monitor")
@router.get("/main index.html")
async def disease_monitor(request: Request):
    return templates.TemplateResponse(request=request, name="main_index.html", context={})

@router.get("/monitor_dashboard")
@router.get("/monitor_dashboard.html")
async def monitor_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="monitor_dashboard.html", context={})

@router.get("/marketplace")
@router.get("/Marketplace_dashboard.html")
async def marketplace(request: Request):
    return templates.TemplateResponse(request=request, name="marketplace_dashboard.html", context={})

@router.get("/predictions")
@router.get("/predictions.html")
async def predictions(request: Request):
    return templates.TemplateResponse(request=request, name="predictions.html", context={})

@router.get("/history")
@router.get("/history.html")
async def history(request: Request):
    return templates.TemplateResponse(request=request, name="history.html", context={})

@router.get("/what_to_grow")
@router.get("/what_to_grow.html")
async def what_to_grow(request: Request):
    return templates.TemplateResponse(request=request, name="what_to_grow.html", context={})

@router.get("/chatbot")
@router.get("/Chat Bot.html")
async def chatbot(request: Request):
    return templates.TemplateResponse(request=request, name="Chat Bot.html", context={})

@router.get("/gemini_info")
@router.get("/index for gemini.html")
async def gemini_info(request: Request):
    return templates.TemplateResponse(request=request, name="index for gemini.html", context={})

@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse(request=request, name="register.html", context={"form": {}}) # form mock for template compat

@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"form": {}}) # form mock for template compat

@router.get("/smart_crop_advisor")
async def render_smart_crop_advisor(request: Request):
    return templates.TemplateResponse(request=request, name="smart_crop_advisor.html", context={"result": None, "status": None})

@router.post("/smart_crop_advisor")
async def handle_smart_crop_advisor(request: Request):
    try:
        form_data = await request.form()
        district = form_data.get("district", "").strip()
        taluk = form_data.get("taluk", "").strip()
        
        import smart_crop_model
        import chatgpt_service
        recommendations, status = smart_crop_model.smart_recommendation(district, taluk)
        
        if recommendations:
            crop_names = [item["crop"] for item in recommendations]
            insights = chatgpt_service.get_crop_market_insights(district, taluk, crop_names)
            for item in recommendations:
                crop_key = item["crop"].upper().strip()
                if crop_key in insights:
                    item["sales_trend"] = insights[crop_key]["sales_trend"]
                    item["market_price"] = insights[crop_key]["market_price"]
        
        return templates.TemplateResponse(
            request=request, 
            name="smart_crop_advisor.html", 
            context={
                "result": recommendations,
                "status": status,
                "district": district,
                "taluk": taluk
            }
        )
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        return templates.TemplateResponse(
            request=request, 
            name="smart_crop_advisor.html", 
            context={
                "result": None,
                "status": f"SERVER ERROR: {error_msg}",
                "district": "",
                "taluk": ""
            }
        )

FESTIVAL_DATA = {

    "January": {
        "Makar Sankranti": {
            "crops": ["Sugarcane", "Sesame", "Groundnut", "Ragi"],
            "flowers": ["Marigold"],
            "leaves": []
        },
        "Pongal": {
            "crops": ["Rice", "Sugarcane", "Turmeric"],
            "flowers": ["Jasmine"],
            "leaves": []
        }
    },

    "February": {
        "Maha Shivratri": {
            "crops": ["Banana", "Coconut"],
            "flowers": ["Datura", "Jasmine"],
            "leaves": ["Bilva Leaves"]
        }
    },

    "March": {
        "Ugadi": {
            "crops": ["Mango", "Neem", "Rice"],
            "flowers": ["Jasmine", "Marigold"],
            "leaves": ["Neem Leaves", "Mango Leaves"]
        },
        "Holi": {
            "crops": ["Maize", "Groundnut"],
            "flowers": ["Palash"],
            "leaves": []
        }
    },

    "April": {
        "Ramzan": {
            "crops": ["Rice", "Wheat"],
            "flowers": [],
            "leaves": []
        }
    },

    "May": {
        "Eid": {
            "crops": ["Rice", "Wheat", "Turmeric", "Chili"],
            "flowers": ["Rose"],
            "leaves": []
        }
    },

    "June": {
        "Kharif Sowing Season": {
            "crops": ["Paddy", "Maize", "Ragi", "Turmeric"],
            "flowers": ["Jasmine"],
            "leaves": []
        }
    },

    "July": {
        "Monsoon Farming": {
            "crops": ["Ragi", "Maize", "Paddy"],
            "flowers": ["Jasmine"],
            "leaves": []
        }
    },

    "August": {
        "Varalakshmi Vrata": {
            "crops": ["Rice", "Coconut"],
            "flowers": ["Jasmine", "Lotus"],
            "leaves": ["Mango Leaves"]
        },
        "Krishna Janmashtami": {
            "crops": ["Rice", "Coconut"],
            "flowers": ["Tulsi", "Jasmine"],
            "leaves": ["Tulsi Leaves"]
        }
    },

    "September": {
        "Ganesh Chaturthi": {
            "crops": ["Rice", "Coconut"],
            "flowers": ["Marigold", "Lotus"],
            "leaves": ["Betel Leaves", "Durva Grass"]
        }
    },

    "October": {
        "Navratri": {
            "crops": ["Ragi", "Rice"],
            "flowers": ["Marigold", "Jasmine"],
            "leaves": []
        },
        "Mysuru Dasara": {
            "crops": ["Rice", "Maize", "Sugarcane"],
            "flowers": ["Marigold"],
            "leaves": ["Banni Leaves"]
        }
    },

    "November": {
        "Diwali": {
            "crops": ["Groundnut", "Sugarcane", "Ragi"],
            "flowers": ["Marigold", "Rose"],
            "leaves": ["Mango Leaves"]
        }
    },

    "December": {
        "Winter Season": {
            "crops": ["Wheat", "Chili", "Vegetables"],
            "flowers": ["Rose"],
            "leaves": []
        }
    }
}

@router.get("/festival")
@router.get("/festival.html")
async def festival(request: Request, month: str = None):
    now = datetime.datetime.now()
    start_month = now.month
    
    if month:
        try:
            start_month = datetime.datetime.strptime(month, "%B").month
        except ValueError:
            pass # fallback to current month
            
    months_to_show = []
    festival_data_to_show = {}
    all_crops = set()
    
    for i in range(3):
        month_index = (start_month - 1 + i) % 12 + 1
        month_name = datetime.date(2000, month_index, 1).strftime('%B')
        months_to_show.append(month_name)
        month_festivals = FESTIVAL_DATA.get(month_name, {})
        festival_data_to_show[month_name] = month_festivals
        for details in month_festivals.values():
            all_crops.update(details.get("crops", []))

    # Fetch growing info for all unique crops from the API
    crop_info = get_crop_growing_info(list(all_crops))

    return templates.TemplateResponse(
        request=request, 
        name="festival.html", 
        context={
            "months": months_to_show,
            "festival_data": festival_data_to_show,
            "crop_info": crop_info
        }
    )
