from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan_events(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan_events)
