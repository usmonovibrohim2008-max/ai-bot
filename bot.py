import os, asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from anthropic import AsyncAnthropic

bot = Bot(os.environ["BOT_TOKEN"])
dp = Dispatcher()
ai = AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

history = {}

@dp.message(CommandStart())
async def start(m: types.Message):
    history[m.from_user.id] = []
    await m.answer("Salom! Savolingni yoz.")

@dp.message()
async def chat(m: types.Message):
    if not m.text:
        return
    h = history.setdefault(m.from_user.id, [])
    h.append({"role": "user", "content": m.text})
    r = await ai.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1000,
        system="Sen foydali yordamchisan. Foydalanuvchi qaysi tilda yozsa, shu tilda javob ber.",
        messages=h[-20:],
    )
    text = r.content[0].text
    h.append({"role": "assistant", "content": text})
    await m.answer(text)

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
