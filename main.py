from aiogram import Bot, executor, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


from score_parser import ClientScore
from Parsing import Client
from message import MESSAGE


Token = '5579385466:AAEEOqPzmxq-pgHfyP5LlB9PCm9VXM1fF5g'

bot = Bot(token=Token)
dp = Dispatcher(bot)
row = ['1', '2', '3', '4', '5', '6', '7', '8']


@dp.message_handler(commands=['start'])
async def start_message(message: Message):
    await bot.send_message(message.from_user.id, MESSAGE['start'])


@dp.message_handler(commands=['help'])
async def help_user(message: Message):
    await bot.send_message(message.from_user.id, MESSAGE['help'])


@dp.message_handler(commands=['timetable'])
async def timetable_name(message: types.Message):
    parser_score = ClientScore()
    text_score = parser_score.run()
    text_score = text_score[16::]
    parser = Client()
    text = parser.run()
    text = text[16::]
    markup = InlineKeyboardMarkup()
    for item_1 in range(0, len(text)):
        text_score[item_1] = str(text_score[item_1]).replace("'", "").replace("[", "").replace("]", "")
        text[item_1] = str(text[item_1]).replace("'", "").replace("[", "").replace("]", "")
        button = InlineKeyboardButton(text=f'{str(text[item_1])} Счёт: '
                                           f'{text_score[item_1]}', callback_data=str(row[item_1]))
        markup.add(button)

    await bot.send_message(message.chat.id, MESSAGE['math'], reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == '1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)


if __name__ == '__main__':
    executor.start_polling(dp)

