import asyncio
from aiogram import Dispatcher, types, Bot, executor
import logging
from trackers.exer_trackers import squats_tracker, pushups_tracker
import json
with open("../utils/config.json") as file:
    data = json.load(file)

TOKEN = data['TOKEN']


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)
name = None
pushups = 0
squats = 0


async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command='/train', description='Начать тренировку'),
        types.BotCommand(command='/info', description='Описание возможностей')
    ]
    await bot.set_my_commands(commands)


@dp.message_handler(commands='block')
async def cmd_block(message: types.Message):
    await asyncio.sleep(10.0)
    await message.reply('Бан')


@dp.message_handler(commands='info')
async def starter(message: types.Message):
    await bot.send_message(message.chat.id, '''введите команду /train для начала тренировки, затем введите свое имя
    ''') 


@dp.message_handler(commands=['отжимания'], content_types=[types.ContentType.VIDEO], commands_ignore_caption=False)
async def video(message: types.Message):
    global pushups, squats
    reworker = pushups_tracker
    video = await message.video.download()
    pu = reworker.track_pushups(video.name)
    pushups += pu
    await message.reply('кол-во отжиманий:' + str(pu))
    await bot.send_message(message.chat.id, f'общее количество отжиманий у {name}: {pushups} ')


@dp.message_handler(commands=['приседания'], content_types=[types.ContentType.VIDEO], commands_ignore_caption=False)
async def video(message: types.Message):
    global squats
    reworker = squats_tracker
    video = await message.video.download()
    sq = reworker.squat_track(video.name)
    squats += sq
    await message.reply('кол-во приседаний:' + str(sq))
    await bot.send_message(message.chat.id, f'общее количество приседаний у {name}: {squats} ')


@dp.message_handler(commands='train')
async def train(message: types.Message):
    await message.reply('Введите имя')


@dp.message_handler(content_types=[types.ContentType.TEXT])
async def name(message: types.Message):
    global name
    name = message.text
    if name in ['вова', 'витя', 'игорь']:
        await message.reply(name + ', отправьте видео с выполнением 3 отжиманий' +
                            '\nи трех приседаний')
    else:
        await message.reply('вас нет в базе:(')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


import logging
import inspect
def log(lvl=logging.DEBUG):
    log_name = inspect.stack()[1][3]
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)
    hanlder = logging.FileHandler('alog.log', mode='w')
    hanlder.setLevel(lvl)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s',
                                  datefmt='%m/%d/%Y %I:%M:%S %p')
    hanlder.setFormatter(formatter)
    logger.addHandler(hanlder)

    return logger

    
    while True:
        print('hello')

    