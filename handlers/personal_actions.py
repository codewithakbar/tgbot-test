import asyncio
import io
import json

from PIL import Image, ImageDraw
import requests
from io import BytesIO

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hunderline, hpre, hlink, escape_md

from dispatcher import dp, bot
from handlers.send_photo_with_logo import send_news_with_logo
from parsing.main import check_news_update


# Personal actions goes here (bot direct messages)
# Here is some example !ping command ...
@dp.message_handler(is_owner=True, commands="ping", commands_prefix="!/")
async def cmd_ping_bot(message: types.Message):
    await message.reply("<b>👊 Up & Running!</b>\n\n")


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):


    kb = [
        [
            types.KeyboardButton(text="Все новости"),
            types.KeyboardButton(text="Свежие новости"),
        ],
        [types.KeyboardButton(text="Последние 5 новостей")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await message.answer(f"Hello yopta: {message.from_user.full_name}", reply_markup=keyboard)


@dp.message_handler(Text(equals="Все новости"))
async def get_all_news(message: types.Message):
    with open("news_dict.json", encoding="utf-8") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items()):
        url = "https://t.me/SatYouNews"
        news =f"{hbold(v['article_title'])}\n\n" \
               f"<b><a href='{url}'>SatYou!</a></b>\n"

        chat_id = message.chat.id
        photo_path = v["article_img"]

        await send_news_with_logo(chat_id, photo_path, news)


@dp.message_handler(Text(equals="Последние 5 новостей"))
async def get_all_news(message: types.Message):
    with open("news_dict.json", encoding="utf-8") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[:-5]:
        url = "https://t.me/SatYouNews"
        news = f"{hbold(v['article_title'])}\n\n" \
               f"<b><a href='{url}'>SatYou!</a></b>\n"

        chat_id = message.chat.id
        photo_path = v["article_img"]

        await send_news_with_logo(chat_id, photo_path, news)



async def news_every_minute():
    while True:
        fresh_news = check_news_update()
        user_id = 933986259

        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                news = f"{hbold(v['article_date_timestamp'])}\n" \
                    f"{hlink(v['article_title'], v['article_url'])}"

                photo_path = v["article_img"]

                await send_news_with_logo(user_id, photo_path, news)

        else:
            await bot.send_message(user_id, text="Пока нет свежих новостей...")

        await asyncio.sleep(60)