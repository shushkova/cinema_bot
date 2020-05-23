import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.bot import api
import aiohttp
import random
from time import sleep
from parser import KinopoiskParser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

proxy_host = 'socks5://178.128.203.1:1080'
proxy_credentials = 'student:TH8FwlMMwWvbJF8FYcq0'

if proxy_credentials:
    login, password = proxy_credentials.split(':')
    proxy_auth = aiohttp.BasicAuth(login=login, password=password)
else:
    proxy_auth = None

bot = Bot(token='1183112339:AAERFnZ5g8dMVph2dMKQeE8UZDjmIHPZZWQ',
          proxy=proxy_host, proxy_auth=proxy_auth)
dp = Dispatcher(bot)


@dp.message_handler(commands=['help'])
async def send_menu(message: types.Message):
    """отправиь список команд бота"""
    await message.reply(
        text="""
        Это CinemaBot. Выводит инфомацию о фильмах и сериалах. Также можно получить ссылки на просмотр фильмов и трейлеров к сериалам\n
        Мои команды: 
        /start - приветсвенное сообщение
        /help -- увидеть помощь"""
    )


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    """отправиь список команд бота"""
    await message.reply("Привет!\nЯ - CinemaBot!\nВведите название фильма для получения информации.")
    # await send_menu(message=message)


"""
@dp.message_handler(content_types=types.ContentType.TEXT)
async def do_echo(message: types.Message):
    text = message.text
    if text:
        await message.reply(text=text)
"""

@dp.message_handler(content_types=types.ContentType.TEXT)
async def search_film(message: types.Message):
    text = message.text
    if text:
        p = KinopoiskParser()
        # sleep(1 + random.randint(0, 20) / 10)
        text = p.parse_all(query=text)
        logger.info(f'text: {text}')
        try:
            try:
                if text["year"]:
                    await message.reply_photo(text["image_link"],
                                              caption=f'Год: {text["year"]}\nСтрана: {text["country"]}\n'
                                                      f'Слоган: {text["slogan"]}\nСсылка '
                                                      f'для просмотра: {text["link"]}\n')
            except:
                await message.reply('Фильм не найден.')
        except:
            await message.reply('Надо немного подождать. Кинопоиск заблокировал ip')


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
