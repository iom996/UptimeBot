import asyncio, aiohttp, logging, dotenv
from os import getenv

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Настройка логов
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s",
    filename="bot.log",
    filemode="a"
)

dotenv.load_dotenv()

TOKEN = getenv("token")  # Убедись, что у тебя переменная окружения `token` задана

# FSM состояния
class Form(StatesGroup):
    web = State()
    interval = State()

dp = Dispatcher()
monitoring_tasks = {}  # Словарь для отслеживания задач по user_id


# /start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    logging.info(f"User {message.from_user.id} started a bot")
    await message.answer(
        "👋 Hello! I’m Uptime — your personal website monitoring assistant.\n"
        "To start monitoring, send /uptime"
    )


# /uptime — старт отслеживания
@dp.message(Command("uptime"))
async def command_uptime(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.web)
    await message.answer(
        "🌍 Great! Now, please send the full URL of the website you want me to monitor "
        "(e.g., `https://example.com`)."
    )


# /cancel — остановка отслеживания
@dp.message(Command("cancel"))
async def cancel_uptime(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    task = monitoring_tasks.get(user_id)
    if task:
        task.cancel()
        del monitoring_tasks[user_id]
        await message.answer(
            "🛑 Monitoring stopped. Let me know if you want to start again!",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer("ℹ️ There's no active monitoring to cancel.")
    await state.clear()


# Получение URL
@dp.message(Form.web)
async def get_web(message: Message, state: FSMContext) -> None:
    await state.update_data(web=message.text)
    await state.set_state(Form.interval)
    await message.answer(
        "🕒 How often should I check the website?\n\n"
        "Please enter the interval in minutes (e.g., `5`)."
    )


# Получение интервала
@dp.message(Form.interval)
async def get_interval(message: Message, state: FSMContext) -> None:
    try:
        interval = int(message.text.strip())
        if interval <= 0:
            raise ValueError
    except ValueError:
        await message.answer(
            "⚠️ That doesn't look like a valid number.\n"
            "Please enter the interval in minutes, using digits only (e.g. `15`)."
        )
        return

    data = await state.get_data()
    web = data.get("web")
    await state.clear()

    await message.answer(
        f"✅ All set! I will now monitor:\n"
        f"🔗 URL: {web}\n"
        f"⏱ Interval: every {interval} minutes\n\n"
        f"You’ll be notified if the website becomes unavailable.\n"
        f"To stop monitoring, press /cancel",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="/cancel")]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )

    # Стартуем отдельную задачу
    task = asyncio.create_task(start_monitoring(web, interval, message))
    monitoring_tasks[message.from_user.id] = task


# Мониторинг
async def start_monitoring(web: str, interval: int, message: Message):
    try:
        while True:
            try:
                is_up = await check_website(web)
                if is_up:
                    await message.answer(f"✅ {web} is online.")
                else:
                    await message.answer(f"⚠️ {web} seems to be down or unresponsive.")
            except Exception as e:
                logging.exception("Error during uptime check")
                await message.answer(f"❌ Error while checking {web}: {e}")

            await asyncio.sleep(interval * 60)
    except asyncio.CancelledError:
        logging.info(f"Monitoring for {web} was cancelled.")
        await message.answer("🛑 Monitoring task has been stopped.")
        return


# Проверка сайта
async def check_website(web: str) -> bool:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(web, timeout=5) as response:
                return response.status == 200
    except:
        return False


# Старт бота
async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.info("Bot is starting...")
    asyncio.run(main())
