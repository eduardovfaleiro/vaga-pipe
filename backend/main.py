from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv
import asyncio
from services.outbox_worker import run_outbox_worker
from api import auth, users, jobs, sync

load_dotenv()

limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])
app = FastAPI(title="Vaga Pipe API")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(jobs.router)
app.include_router(sync.router)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_outbox_worker())


@app.get("/")
async def root():
    return {"message": "Vaga Pipe API is running"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}
