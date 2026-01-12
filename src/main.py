import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command

# Токен бота
TOKEN = '8258230917:AAEMnDBaxTaitbTbQp1z_doBZJ-TPNEj778'

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Состояние пользователя: пройденные игры
user_games = {}

# Мини-игры: список игр
games = ['quiz', 'guess_number']

# Викторина: вопросы и ответы
quiz_questions = [
    {"question": "Столица России?", "answer": "Москва"},
    {"question": "2 + 2 = ?", "answer": "4"}
]

# Угадай число: случайное число от 1 до 10
import random

@dp.message(Command("start"))
async def start_command(message: Message):
    user_id = message.from_user.id
    user_games[user_id] = {'completed': []}
    await message.reply("Привет! Давай поиграем в мини-игры. Напиши /play для начала.")

@dp.message(Command("play"))
async def play_command(message: Message):
    user_id = message.from_user.id
    if user_id not in user_games:
        user_games[user_id] = {'completed': []}
    
    if len(user_games[user_id]['completed']) < len(games):
        next_game = games[len(user_games[user_id]['completed'])]
        if next_game == 'quiz':
            user_games[user_id]['current_game'] = 'quiz'
            user_games[user_id]['quiz_index'] = 0
            await message.reply(f"Викторина! Вопрос: {quiz_questions[0]['question']}")
        elif next_game == 'guess_number':
            user_games[user_id]['current_game'] = 'guess_number'
            user_games[user_id]['number'] = random.randint(1, 10)
            await message.reply("Угадай число от 1 до 10!")
    else:
        await message.reply("*братан прости что так поступил, давай начнем все сначала, и кстати и удалился из км докса и вообще осинт тд и тп, братан давай дружить как раньше*")

@dp.message()
async def handle_message(message: Message):
    user_id = message.from_user.id
    if user_id in user_games and 'current_game' in user_games[user_id]:
        game = user_games[user_id]['current_game']
        if game == 'quiz':
            index = user_games[user_id]['quiz_index']
            if message.text.lower() == quiz_questions[index]['answer'].lower():
                user_games[user_id]['completed'].append('quiz')
                del user_games[user_id]['current_game']
                del user_games[user_id]['quiz_index']
                await message.reply("Правильно! Напиши /play для следующей игры.")
            else:
                await message.reply("Неправильно. Попробуй снова.")
        elif game == 'guess_number':
            try:
                guess = int(message.text)
                if guess == user_games[user_id]['number']:
                    user_games[user_id]['completed'].append('guess_number')
                    del user_games[user_id]['current_game']
                    del user_games[user_id]['number']
                    await message.reply("Угадал! Напиши /play для следующей игры.")
                elif guess < user_games[user_id]['number']:
                    await message.reply("Больше!")
                else:
                    await message.reply("Меньше!")
            except ValueError:
                await message.reply("Введи число!")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())