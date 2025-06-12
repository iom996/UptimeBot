from aiogram import Bot, Dispatcher,F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage import redis
import asyncio
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


@dp.message(Form.web)
async def get_web(message: Message, state: FSMContext) -> None:

    await state.update_data(web=message.text)
    await state.set_state(Form.interval)
    await message.answer('Well, what interval?(minutes)')

@dp.message(Form.interval)
async def get_interval(message: Message, state: FSMContext) -> None:
   await state.update_data(interval=int(message.text))
   data = await state.get_data()
   web = data.get("web")
   interval = message.text
   text = f"{web}, {interval}"

   await message.answer(text=text)
   await state.clear()

async def storage():
   main = main

@dp.message
async def main() -> None:
  bot = Bot(token=TOKEN)

  await dp.start_polling(bot)

if __name__ == '__main__' :
  asyncio.run(main())