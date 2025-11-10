import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .Database.database import create_db_and_table
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on application startup
    print("INFO:     Application startup...")
    print("INFO:     Calling create_db_and_table()...")
    
    # This is the line that runs your function
    create_db_and_table()
    
    print("INFO:     Tables should be created (if they don't exist).")
    yield
    # Code to run on application shutdown
    print("INFO:     Application shutdown...")

# Tell FastAPI to use this lifespan function
app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "This is the Server"}








