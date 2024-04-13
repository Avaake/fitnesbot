from aiogram.types import Update
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from fitnesbot import start_bot
from .user import router as user_router

app = FastAPI(lifespan=start_bot.lifespan)
app.include_router(user_router)
app.mount("/static", StaticFiles(directory="web/static"), name="static")


@app.post("/webhook", tags=["root"])
async def webhook(request: Request) -> None:
    update = Update.model_validate(await request.json(), context={"bot": start_bot.bot})
    await start_bot.dp.feed_update(start_bot.bot, update)
