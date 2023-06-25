from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text, Command

from config import TOKEN
from utils import get_random_num

bot = Bot(TOKEN)
dp = Dispatcher(bot)

ATTEMPTS = 5
user = {
    'in_game': False,
    'secret_number': 0,
    'attempts': 0,
    'total_games': 0,
    'win_games': 0
}


async def cmd_start(message: types.Message):
    await message.answer('Добрый день, какие планы на сегодня?\n'
                         'Сыграем в игру? отправьте /help\n'
                         'для получения правил')


async def cmd_help(message: types.Message):
    await message.answer(f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
                         f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
                         f'попыток\n\nДоступные команды:\n/help - правила '
                         f'игры и список команд\n/cancel - выйти из игры\n'
                         f'/stat - посмотреть статистику\n\nДавай сыграем?')


async def cmd_stat(message: types.Message):
    await message.answer(f'У вас {user["total_games"]} сыгранных игр,\nиз них {user["win_games"]} - выиграно !!!')


async def cmd_cancel(message: types.Message):
    if user['in_game'] is True:
        await message.answer('Игра остановлена, жду вашего возвращения')
        user['in_game'] = False
    else:
        await message.answer('Мы с вами и не играли, исправим это?')


async def play_start(message: types.Message):
    if not user['in_game']:
        await message.answer('Я загадал число от 1 до 100. Отгадайте')
        user['in_game'] = True
        user['secret_number'] = get_random_num()
        user['attempts'] = ATTEMPTS

    else:
        await message.answer('Во время игры ожидаю ответ 1-100, или команды:\n\n'
                             '/cancel\n'
                             '/stat')


async def check_answer(message: types.Message):
    if message.text == user['secret_number']:
        await message.answer('Вы угадали, сыграем еще?')
        user['in_game'] = False
        user['win_games'] += 1
    else:
        user["attempts"] -= 1
        if user["attempts"] >= 1:
            verdict = 'больше' if int(message.text) > user['secret_number'] else 'меньше'
            await message.answer(f'Вы не угадали, увас осталась {user["attempts"]} попыток/ка\n'
                                 f'Ваше число {message.text} {verdict} загаданного')
        else:
            user['in_game'] = False
            await message.answer('У вас закончились попытки, вы проиграли ((\n'
                                 f'Я загадывал число {user["secret_number"]}\n'
                                 'Сыграем еще?')


async def final(message: types.Message):
    await message.reply('Для этого запроса нет обработчика')


def run_bot():
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(cmd_help, commands=['help'])
    dp.register_message_handler(cmd_stat, commands=['stat'])
    dp.register_message_handler(cmd_cancel, commands=['cancel'])
    dp.register_message_handler(play_start, Text(['Да', 'Go', 'Начать', 'Поехали']))
    dp.register_message_handler(check_answer, Text([str(i) for i in range(100)]))
    dp.register_message_handler(final)
    print('OK')
    executor.start_polling(dispatcher=dp)


if __name__ == '__main__':
    print('Running Bot...')
    run_bot()
