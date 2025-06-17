import pytest
from aiogram import Bot
from aiogram.types import Message, User, Chat
from main import dp  # Импорт твоего Dispatcher из main.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.mark.asyncio
async def test_start_handler(monkeypatch):
    sent_messages = []

    async def fake_answer(text, **kwargs):
        sent_messages.append(text)

    user = User(id=12345, is_bot=False, first_name="Tester")
    chat = Chat(id=12345, type="private")
    message = Message(message_id=1, from_user=user, chat=chat, text="/start", date=None)

    monkeypatch.setattr(message, "answer", fake_answer)

    await dp.feed_update(message)

    assert any("Hello" in msg for msg in sent_messages)
