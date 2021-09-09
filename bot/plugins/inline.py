"""
vcVideoPlayer, Telegram Video Chat Bot
Copyright (c) 2021  Zaute Km

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

import asyncio
from config import Config
from pyrogram import Client, errors
from pyrogram.handlers import InlineQueryHandler
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from youtubesearchpython import VideosSearch

REPLY_MESSAGE = Config.REPLY_MESSAGE

buttons = [
            [
                InlineKeyboardButton("🗣️ Feedback", url="https://t.me/zautebot"),
                InlineKeyboardButton("Channel 📢", url="https://t.me/tgbotsproject"),
            ],
            [
                InlineKeyboardButton("🤖 Deploy to Heroku 🤖", url="https://heroku.com/deploy?template=https://github.com/ZauteKm/vcVideoPlayer"),
            ]
         ]

@Client.on_inline_query()
async def search(client, query):
    answers = []
    if query.query == "ZAUTE_KM":
        answers.append(
            InlineQueryResultArticle(
                title="Deploy Own Video Player Bot",
                input_message_content=InputTextMessageContent(f"{REPLY_MESSAGE}\n\n<b>© Powered By : \n@ZauteKm | @tgbotsproject 👑</b>", disable_web_page_preview=True),
                reply_markup=InlineKeyboardMarkup(buttons)
                )
            )
        await query.answer(results=answers, cache_time=0)
        return
    string = query.query.lower().strip().rstrip()
    if string == "":
        await client.answer_inline_query(
            query.id,
            results=answers,
            switch_pm_text=("Search a YouTube Videos!"),
            switch_pm_parameter="help",
            cache_time=0
        )
    else:
        videosSearch = VideosSearch(string.lower(), limit=50)
        for v in videosSearch.result()["result"]:
            answers.append(
                InlineQueryResultArticle(
                    title=v["title"],
                    description=("Duration: {} Views: {}").format(
                        v["duration"],
                        v["viewCount"]["short"]
                    ),
                    input_message_content=InputTextMessageContent(
                        "/stream https://www.youtube.com/watch?v={}".format(
                            v["id"]
                        )
                    ),
                    thumb_url=v["thumbnails"][0]["url"]
                )
            )
        try:
            await query.answer(
                results=answers,
                cache_time=0
            )
        except errors.QueryIdInvalid:
            await query.answer(
                results=answers,
                cache_time=0,
                switch_pm_text=("❌ No Results Found!"),
                switch_pm_parameter="",
            )


__handlers__ = [
    [
        InlineQueryHandler(
            search
        )
    ]
]
