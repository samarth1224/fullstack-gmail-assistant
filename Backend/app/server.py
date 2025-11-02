import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .authentication import authentication
from .router import users, websocket


APP_NAME = 'gmail_agent'


app  = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://fullstack-gmail-assistant.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(authentication.router)
app.include_router(websocket.router)

@app.get("/")
async def root():
    return {"message": "This is the Server"}








