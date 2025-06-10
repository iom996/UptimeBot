from aiogram import Bot, Dispatcher, fsm
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from time import sleep
import asyncio
from os import getenv
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

TOKEN = getenv("token")

class Form(StatesGroup):

    web = State()

    interval = State()

dp = Dispatcher()
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
  await message.answer("Hello i am UpTime bot to Uptime send /uptime")

@dp.message(Command("uptime"))
async def command(message: Message, state: FSMContext) -> None :
 await state.set_state(Form.web)
 await message.answer(

        "What is your web for Uptime?",

        reply_markup=ReplyKeyboardRemove(),

    )
 #buttons = [[KeyboardButton(text='Cancel input')]]
 #keyboard = ReplyKeyboardMarkup(keyboard=buttons)
 #await message.answer('ok', reply_markup=keyboard)

async def main() -> None:
  bot = Bot(token=TOKEN)

  await dp.start_polling(bot)

if __name__ == '__main__' :
  asyncio.run(main())