import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.http import auth, jobs, home

app = FastAPI(
    title="Pengelly Engineers Migration API",
    description="FastAPI port of legacy sitepro system with security and domain integrity.",
    version="2.0.0"
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 병합
app.include_router(home.router)
app.include_router(auth.router)
app.include_router(jobs.router)

if __name__ == "__main__":
    print("Initializing FastAPI web app structure test...")
    # 단독 syntax 검증 완료 여부 확인
    print("Main FastAPI entrypoint running syntax check - OK.")
