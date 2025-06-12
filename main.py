from aiogram import Bot, Dispatcher,F, html
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio, typing
from os import getenv
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

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
 await message.answer("What is your web for Uptime?")
 #buttons = [[KeyboardButton(text='Cancel input')]]
 #keyboard = ReplyKeyboardMarkup(keyboard=buttons)
 #await message.answer('ok', reply_markup=keyboard)

@dp.message(Form.web)
async def interval(message: Message, state: FSMContext) -> None:

    await state.update_data(web=message.text)
    await state.set_state(Form.interval)
    await message.answer('Well, what interval?(minutes)')

@dp.message(Form.interval)
async def uptiming(message: Message, state: FSMContext) -> None:
   data = await state.get_data()
   await state.update_data(interval=int(message.text))
   await state.clear()
   await show_summary(message = message, data=data)

async def show_summary(message: Message, data: typing.Dict[str, typing.Any]) -> None:

    web = data["web"]

    interval = data.get("interval", None)

    text = f"{web}, {interval} "

    await message.answer(text=text)



async def main() -> None:
  bot = Bot(token=TOKEN)

  await dp.start_polling(bot)

if __name__ == '__main__' :
  asyncio.run(main())