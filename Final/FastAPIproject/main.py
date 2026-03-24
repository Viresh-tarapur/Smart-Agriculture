import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import engine, Base
from routes import pages, gps, auth

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Plant Disease Detection API")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(pages.router)
app.include_router(gps.router, prefix="/api")
app.include_router(auth.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
