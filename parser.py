# # encoding = 'utf-8'.
from datetime import datetime
import snscrape.modules.telegram as stela
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import requests
from bs4 import BeautifulSoup
import re

url='https://ligovka.ru/detailed/usd?tab=200' 
query='doolarharat' #it work if chanel have more then 1000 folowers
tehran='dollar_tehran3bze' #it work if chanel have more then 1000 folowers
API_TOKEN = '[print you token]'
ADMIN ='136734651'
ADMIN ='6072975817'
curent_time=datetime.now()
logging.basicConfig(level=logging.INFO)
q=requests.get(url)
result=q.content
# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

soup=BeautifulSoup(result,'lxml')
table1=soup.find("table",{"class" : "table_course"})
with open('f.txt','w',encoding='utf-8') as f:
    for i in table1.find_all('td',):
        f.write(i.text+'\n')
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    for msg in stela.TelegramChannelScraper(query).get_items():
        for msgt in stela.TelegramChannelScraper(tehran).get_items():
            if curent_time.hour>=10:
                while curent_time.hour<20:
                    try:
                        for i in range(1000000000):
                            with open("f.txt", "r",encoding="utf-8") as file:
                                # take use 9-10 line
                                contents = file.readlines()
                                str1 = contents[9]
                                str2 = contents[10]
                                ru=' 🇺🇸  🇷🇺 نرخ دلار به روبل مسکو\n خرید: \n{}  فروش: \n {}'.format(str1,str2) 
                                doll_teh=re.sub('\D', '', msg.content) 
                                af='🇺🇸   🇦🇫 نرخ دلار به تومان هرات\n '+doll_teh
                                tom_msk=round(float(doll_teh)/((float(str1)+float(str2))/2),1)
                                tom='🇺🇸  🇷🇺 🇮🇷 نرخ دلار به تومان مسکو\n{}'.format(doll_teh)
                                doll_ir=re.sub('\D', '', msgt.content)
                                ir='🇺🇸 🇮🇷 نرخ دلار به تومان تهران\n {}'.format(doll_ir)                        
                                it=af+'\n'+ir+'\n'+ru+'\n'+tom
                                await bot.send_message(chat_id='@doolarmsk', text=it)
                                await asyncio.sleep(300)
    
                    except TypeError:
                        break  
            else:
                asyncio.sleep(300)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
