import asyncio
import io
import json

from PIL import Image, ImageDraw
import requests
from io import BytesIO

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hunderline, hpre, hlink, text

from dispatcher import dp, bot
from handlers.send_photo_with_logo import send_news_with_logo
from parsing.main import check_news_update

from data.config import CHANNELS


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

    for k, v in sorted(news_dict.items())[:10]:
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

    for k, v in sorted(news_dict.items())[:5]:
        url = "https://t.me/SatYouNews"
        news = f"{hbold(v['article_title'])}\n\n" \
                f"{text(v['article_content'])}\n\n" \
               f"<b><a href='{url}'>SatYou!</a></b>\n"

        chat_id = message.chat.id
        photo_path = v["article_img"]

        await send_news_with_logo(chat_id, photo_path, news)





async def news_every_minute():
    while True:
        fresh_news = check_news_update()
        user_id = (984573662, 933986259)

        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                url = "https://t.me/SatYouNews"
                news = f"{hbold(v['article_title'])}\n\n" \
                    f"{hbold(v['article_content'])}\n\n" \
                f"<b><a href='{url}'>SatYou!</a></b>\n"

                photo_path = v["article_img"]

                for send in user_id:
                    await send_news_with_logo(send, photo_path, news)

        else:
            for send in user_id:
                await bot.send_message(send, text="Пока нет свежих новостей...")

        await asyncio.sleep(60)




@dp.callback_query_handler(text='admin_confirm')
async def confirm_post(call: types.CallbackQuery):
    message = await call.message.edit_reply_markup()
    await message.send_copy(chat_id=CHANNELS[0])


@dp.callback_query_handler(text='admin_cancel')
async def cancel_post(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Bekor qilindi")