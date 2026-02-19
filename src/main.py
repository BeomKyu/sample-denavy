# src/main.py
# FastAPI 앱 진입점 — 인프라 조립 (Infrastructure Wiring)
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import Base, engine
from .user import signup as signup_module


@asynccontextmanager
async def lifespan(app: FastAPI):
    # DB 테이블 자동 생성 (Base.metadata.create_all)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

# 라우터 등록
app.include_router(signup_module.router, prefix="/user", tags=["user"])
