from fastapi import FastAPI, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from apscheduler.schedulers.background import BackgroundScheduler

from messages import log_message, process_messages, inspirational_quote

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_csp_header(request, call_next):
    response = await call_next(request)
    csp_policy = (
        "default-src 'self';"
        "script-src 'self';"
        "style-src 'self' https://fonts.googleapis.com;"
        "font-src 'self' https://fonts.gstatic.com;"
    )
    response.headers["Content-Security-Policy"] = csp_policy
    return response


@app.post("/submit")
async def create_submission(message: Annotated[str, Form()], datetime: Annotated[str, Form()], timezone: Annotated[str, Form()]):
    try:
        log_message(message, datetime, timezone)
    except:
        raise HTTPException(status_code=500, detail="Failed to store message")

app.mount("/", StaticFiles(directory="../client", html=True), name="static")


scheduler = BackgroundScheduler()
scheduler.add_job(process_messages, trigger='cron', hour=6, minute=30)
scheduler.add_job(inspirational_quote, trigger='cron', hour=18, minute=0)
scheduler.start()
