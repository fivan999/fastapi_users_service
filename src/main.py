from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.users.routes import user_router


@asynccontextmanager
async def lifespan_events(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan_events)
app.include_router(user_router)
