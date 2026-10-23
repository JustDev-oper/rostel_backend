import os
import sqlite3
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()
from .database import initialize_database
from .routers import companies, projects, deals, proposals, stats

@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield

app = FastAPI(
    title=os.getenv('APP_NAME', 'Экосистема коммерческого блока Ростелекома'),
    version='1.0.0',
    description='REST API: радар присутствия, инвестиционный навигатор и калькулятор сделок.',
    lifespan=lifespan,
)
origins = [x.strip() for x in os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',') if x.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

@app.exception_handler(sqlite3.IntegrityError)
async def integrity_error(_: Request, exc: sqlite3.IntegrityError):
    return JSONResponse(status_code=409, content={'detail': 'Conflict: duplicate value or referenced entity constraint.', 'reason': str(exc)})

@app.get('/health', tags=['Сервис'])
def health(): return {'status': 'ok'}

app.include_router(companies.router)
app.include_router(projects.router)
app.include_router(deals.router)
app.include_router(proposals.router)
app.include_router(stats.router)
