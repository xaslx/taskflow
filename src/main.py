from fastapi import FastAPI
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):

    yield



def create_app() -> FastAPI:


    app: FastAPI = FastAPI(
        title='TaskFlow',
        description='Система управления бизнесом',
        version='0.1',
    )

    return app