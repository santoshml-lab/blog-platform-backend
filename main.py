from fastapi import FastAPI

from database import Base, engine
from routes.auth import router as auth_router

import models


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Blog Platform API",
    description="RESTful API for a blogging platform with authentication and comments",
    version="1.0.0"
)


# Authentication routes
app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "message": "Blog Platform API is running 🚀"
    }
