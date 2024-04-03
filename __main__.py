import logging

import uvicorn
from aiogram.types import Update
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fitnesbot.runbot import RunBot

start_bot = RunBot()
app = FastAPI(lifespan=start_bot.lifespan)
templates = Jinja2Templates(directory="web/templates")
app.mount("/static", StaticFiles(directory="web/static"), name="static")


@app.get("/calcbzy")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/webhook")
async def webhook(request: Request) -> None:
    update = Update.model_validate(await request.json(), context={"bot": start_bot.bot})
    await start_bot.dp.feed_update(start_bot.bot, update)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                               ' - (Line: %(lineno)d [%(filename)s - %(funcName)s])')
    try:
        uvicorn.run(app)
    except KeyboardInterrupt:
        print('Exit')
