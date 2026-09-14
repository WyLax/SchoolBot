import asyncio

from aiogram import Bot, Dispatcher, types, F, BaseMiddleware
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import LabeledPrice

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from func_base_work import base_work
from func_button import button
from func_photo import photo
from func_menu import menu
from func_save_screen import save_screen
from func_save_menu import save_menu
from func_table import table
from func_day_link import day_link
from func_day_text import day_text

from dotenv import load_dotenv
import os




load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
school_base = 'school_database.db'
admins = {'wylaxx'}
albums = {}

bot = Bot(API_TOKEN)
dp = Dispatcher()


### ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡ ###


class UserMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if not event.text or not event.text.startswith("/start"):
            if event.chat.type == "private":
                await base_work(school_base,f"INSERT OR IGNORE INTO user_data (user_id, first_name, username) VALUES ('{event.chat.id}', '{event.chat.first_name}', '{event.chat.username}')")
            else:
                await base_work(school_base,f"INSERT OR IGNORE INTO user_data (user_id, first_name, username) VALUES ('{event.chat.id}', '{event.chat.title}', '{event.chat.username}')")

        await base_work(school_base, f"UPDATE user_data SET last_activity = CURRENT_TIMESTAMP WHERE user_id = '{event.chat.id}'")


        return await handler(event, data)


dp.message.middleware(UserMiddleware())


### ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡ ###


days_cache = {}

async def init_days():
    print('включение...')

    global days_cache
    days_cache = {
        'test': await table('test'),
        'monday': await table('monday'),
        'tuesday': await table('tuesday'),
        'wednesday': await table('wednesday'),
        'thursday': await table('thursday'),
        'friday': await table('friday'),
    }

    print('включился')


async def check_updates():
    global days_cache


    chat_ids_all = [
        int(item[0])
        for item in await base_work(
            school_base,
            "SELECT user_id FROM user_data WHERE auto_send='вкл'"
        )
    ]


    for day_name, old_data in days_cache.items():
        new_data = await table(day_name)

        if new_data != old_data:
            #print(f'изменения в {day_name}')
            days_cache[day_name] = new_data

            await save_screen(day_name, await day_link(day_name))
            photo_file = await photo(day_name)

            #print(f'{day_name} отправка: {chat_ids_all}')

            for chat_id_all in chat_ids_all:
                try:
                    await bot.send_photo(
                        chat_id_all,
                        photo=photo_file,
                        caption=f"Обновлённое расписание на {await day_text(day_name)}"
                    )
                except:

                    a=1


### ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡ ###


@dp.message(Command('start'))
async def send_welcome(message: types.Message):

    if message.chat.type == "private":

        button1 = KeyboardButton(text="📋 Меню столовой на ближайший день")
        button2 = KeyboardButton(text="🗓 Расписание на любой день")
        button3 = KeyboardButton(text="⚙ Настройки")
        button4 = KeyboardButton(text="👤 Профиль")
        button5 = KeyboardButton(text="💬 Отзыв")

        keyboard = ReplyKeyboardMarkup(keyboard=[
            [button1],
            [button2],
            [button3, button5, button4]
        ], resize_keyboard=True, one_time_keyboard=False)

        if not await base_work(school_base, f"SELECT * FROM user_data WHERE user_id = '{message.chat.id}'"):
            await base_work(school_base, f"INSERT INTO user_data (user_id, first_name, username) VALUES ('{message.chat.id}', '{message.chat.first_name}', '{message.chat.username}')")
            await message.reply(f"Приветик, {message.chat.first_name}, я школьный бот помощник!\n\nМои возможности:\n/start - перезапустить бота\n/info - посмотреть информацию о создателе и о боте\n/table_day - посмотреть расписание на любой день недели\n/menu - посмотреть меню в столовой\n/options - дополнительные настройки\n/profile - посмотреть свой профиль\n/support - поддержать проект\n/feedback - оставить отзыв",reply_markup=keyboard)
            await message.answer(f"Кстати, у меня наконец-то появился собственный сервер, поэтому теперь бот сможет работать 24/7. Спасибо, что пользуешься ботом! ❤️")
        else:
            await message.reply(f"Приветик, {message.chat.first_name}!\n\nМои возможности:\n/start - перезапустить бота\n/info - посмотреть информацию о создателе и о боте\n/table_day - посмотреть расписание на любой день недели\n/menu - посмотреть меню в столовой\n/options - дополнительные настройки\n/profile - посмотреть свой профиль\n/support - поддержать проект\n/feedback - оставить отзыв",reply_markup=keyboard)


    else:
        await message.reply(f"Рад всех видеть в {message.chat.title}, я школьный бот помощник!\n\nМои возможности:\n/start - перезапустить бота\n/info - посмотреть информацию о создателе и о боте\n/table_day - посмотреть расписание на любой день недели\n/menu - посмотреть меню в столовой\n/options - дополнительные настройки\n/profile - посмотреть профиль группы\n/support - поддержать проект")
        if not await base_work(school_base, f"SELECT * FROM user_data WHERE user_id = '{message.chat.id}'"):
            await base_work(school_base, f"INSERT INTO user_data (user_id, first_name, username) VALUES ('{message.chat.id}', 'группа: {message.chat.title}', '{message.chat.username}')")
            await message.answer(f"Кстати, у меня наконец-то появился собственный сервер, поэтому теперь бот сможет работать 24/7. Спасибо, что пользуетесь ботом! ❤️")


### ▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱ ###


@dp.message(Command('options'))
async def options_command_handler(message: types.Message):
    if str(await base_work(school_base, f"SELECT auto_send FROM user_data WHERE user_id='{message.chat.id}'"))[3:-4] == 'вкл':
        item1 = 'авто отправка  🔔'
    else:
        item1 = 'авто отправка  🔕'

    await message.reply("Настройки бота:", reply_markup=button([item1], 1))


### ▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱ ###


@dp.message(Command("table_day"))
async def table_day_command_handler(message: types.Message):
    await message.reply("Выбери день недели", reply_markup=button(["понедельник", "вторник", "среда", "четверг", "пятница"], 1))


### ▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱ ###


@dp.message(Command("info"))
async def info_command_handler(message: types.Message):
    await message.reply(
"""<tg-emoji emoji-id="5422439311196834318">💡</tg-emoji> <b>Информация:<b>
<b>──────────────────────</b>
Создатель бота - @wylaxx
Тестировщик бота - @None\_less
<b>──────────────────────</b>
<tg-emoji emoji-id="5282843764451195532">🖥</tg-emoji> Вся информация о расписаниях берётся с <a href="https://www.22vp.ru">официального сайта школы</a>
<b>──────────────────────</b>
<tg-emoji emoji-id="5443038326535759644">💬</tg-emoji> Пишите свои предложения и пожелания, а также сообщайте об ошибках в отзывах, либо напрямую @wylaxx""",
        parse_mode="HTML",
        disable_web_page_preview=True
    )


### ▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱ ###


@dp.message(Command("profile"))
async def profile_command_handler(message: types.Message):
    if message.chat.type == "private":
        await message.reply(f"""
<tg-emoji emoji-id="5231012545799666522">🔍</tg-emoji> <b>Твой профиль</b>
<b>──────────────────────</b>
<tg-emoji emoji-id="5271604874419647061">🔗</tg-emoji> <b>ID:</b> <code>{message.chat.id}</code>
      <b>Имя:</b> <code>{message.chat.first_name}</code>
<b>──────────────────────</b>
<tg-emoji emoji-id="5424818078833715060">📣</tg-emoji> <b>Авто отправка:</b> <code>{str(await base_work(school_base, f"SELECT auto_send FROM user_data WHERE user_id = '{message.chat.id}'"))[3:-4]}</code>
<b>──────────────────────</b>
_версия бота v1.2 beta_
""", parse_mode="HTML")

    else:
        await message.reply(f"""
<tg-emoji emoji-id="5231012545799666522">🔍</tg-emoji> <b>Профиль группы</b>
<b>──────────────────────</b>
<tg-emoji emoji-id="5271604874419647061">🔗</tg-emoji> <b>ID:</b> <code>{message.chat.id}</code>
<b>Группа:</b> <code>{message.chat.title}</code>
<b>──────────────────────</b>
      <tg-emoji emoji-id="5424818078833715060">📣</tg-emoji> <b>Авто отправка:</b> <code>{str(await base_work(school_base, f"SELECT auto_send FROM user_data WHERE user_id = '{message.chat.id}'"))[3:-4]}</code>
<b>──────────────────────</b>
_версия бота v1.2 beta_
""", parse_mode="HTML")


### ▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱ ###


@dp.message(Command("menu"))
async def menu_command_handler(message: types.Message):
    await message.reply_photo(photo=await menu(), caption=f"Меню известное на данный момент")


### ▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱ ###


@dp.message(Command("upd_menu"))
async def updmenu_command_handler(message: types.Message):
    await save_menu()
    await message.reply('меню обновлено')


### ▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱ ###


@dp.message(Command("upd_table"))
async def updtable_command_handler(message: types.Message):
    
    await save_screen('monday', await day_link('monday'))
    await message.reply('пн обновлено')

    await save_screen('tuesday', await day_link('tuesday'))
    await message.answer('вт обновлено')

    await save_screen('wednesday', await day_link('wednesday'))
    await message.answer('ср обновлено')

    await save_screen('thursday', await day_link('thursday'))
    await message.answer('чт обновлено')

    await save_screen('friday', await day_link('friday'))
    await message.answer('пт обновлено')


### ▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱ ###


@dp.message(Command("stats"))
async def stats_command_handler(message: types.Message):
    if message.chat.username not in admins:
        await message.reply("Эту команду могут использовать только админы бота")
        return

    activity_1day = (await base_work(school_base, "SELECT COUNT(*) FROM user_data WHERE last_activity >= datetime('now', '-1 day')"))[0][0]
    activity_7day = (await base_work(school_base, "SELECT COUNT(*) FROM user_data WHERE last_activity >= datetime('now', '-7 day')"))[0][0]
    activity_30day = (await base_work(school_base, "SELECT COUNT(*) FROM user_data WHERE last_activity >= datetime('now', '-30 day')"))[0][0]
    bot_users = (await base_work(school_base, "SELECT COUNT(*) FROM user_data"))[0][0]


    await message.reply(f"""
📊 *статистика:*
*──────────────────────*
*Всего:* `{bot_users}`
*За день:* `{activity_1day}`
*За неделю:* `{activity_7day}`
*За месяц:* `{activity_30day}`
""", parse_mode="Markdown")


### ▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱ ###


class Feedback(StatesGroup):
    waiting = State()


@dp.message(Command("feedback"))
async def feedback_command(message: types.Message, state: FSMContext):
    if message.chat.type != "private":
        await message.reply("К сожалению оставить отзыв в группе нельзя")
        return

    await message.reply(
        "Просто напиши своё мнение о боте или что ты бы хотел в него добавить, только прошу не балуйся:",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Отмена", callback_data="cancel_feedback")]
            ]
        )
    )

    await state.set_state(Feedback.waiting)


@dp.message(F.text == "💬 Отзыв")
async def feedback_button(message: types.Message, state: FSMContext):
    if message.chat.type != "private":
        await message.reply("К сожалению оставить отзыв в группе нельзя")
        return

    await message.reply(
        "Просто напиши своё мнение о боте или что ты бы хотел в него добавить, только прошу не балуйся:",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Отмена", callback_data="cancel_feedback")]
            ]
        )
    )

    await state.set_state(Feedback.waiting)


@dp.callback_query(F.data == "cancel_feedback")
async def cancel_feedback(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Ну ладно")
    await callback.answer()


@dp.message(Feedback.waiting)
async def process_feedback(message: types.Message, state: FSMContext):
    await state.clear()

    await message.reply("Спасибо за ваш отзыв!")

    await message.bot.send_message(
        -1002377171177,
        f"""
*Отзыв от:* {message.chat.first_name} {message.chat.id}
*──────────────────────*
{message.text}
""",
        parse_mode="Markdown"
    )


### ▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱ ###


class CopyMessage(StatesGroup):
    waiting = State()


@dp.message(Command("sendall"))
async def copy_command(message: types.Message, state: FSMContext):
    if message.chat.username not in admins:
        await message.reply("Эту команду могут использовать только админы бота")
        return

    await message.reply(
        "Напишите ваше сообщение:",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Отмена", callback_data="cancel_sendall")]
            ]
        )
    )

    await state.set_state(CopyMessage.waiting)


@dp.callback_query(F.data == "cancel_sendall")
async def cancel_sendall(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Отправка отменена")
    await callback.answer()


@dp.message(CopyMessage.waiting)
async def copy_message(message: types.Message, state: FSMContext):
    if message.chat.username not in admins:
        return

    done = 0
    not_done = 0

    all_users_id = [
        int(item[0])
        for item in await base_work(
            school_base,
            "SELECT user_id FROM user_data"
        )
    ]

    if message.media_group_id:
        albums.setdefault(message.media_group_id, []).append(message)

        await asyncio.sleep(0.3)

        album = albums.pop(message.media_group_id, None)
        if not album:
            return
        ids = sorted(m.message_id for m in album)

        for user_id in all_users_id:
            try:
                await message.bot.forward_messages(
                    chat_id=user_id,
                    from_chat_id=message.chat.id,
                    message_ids=ids
                )
                done += 1
            except:
                not_done += 1

    else:
        for user_id in all_users_id:
            try:
                await message.forward(chat_id=user_id)
                done += 1
            except:
                not_done += 1

    await message.reply(f"удачных отправок: {done} из {done + not_done}")

    await state.clear()


### ▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱ ###


@dp.message(Command("support"))
async def supports(message: types.Message):

    buttons = []

    for stars in [10, 25, 50, 100]:
        invoice_link = await bot.create_invoice_link(
            title="Поддержка проекта",
            description=f"Поддержка проекта на {stars}",
            payload=f"support_{stars}",
            currency="XTR",
            prices=[
                LabeledPrice(
                    label="Поддержка",
                    amount=stars
                )
            ]
        )

        buttons.append(
            InlineKeyboardButton(
                text=f"{stars}", icon_custom_emoji_id={
            10: "5920433463428650761",
            25: "5920433463428650761",
            50: "5920108570627544286",
            100: "5920281855378068765"
        }[stars],
                url=invoice_link
            )
        )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [buttons[0], buttons[1]],
            [buttons[2], buttons[3]]
        ]
    )

    await message.reply(f"""
<tg-emoji emoji-id="5267102644886853973">❤️</tg-emoji> <b>Поддержать проект</b>
<b>──────────────────────</b>
Если бот вам понравился, вы можете поддержать его развитие звёздами либо же через СБП. Любая поддержка очень ценна и помогает поддерживать работу бота

Выберите сумму поддержки:
""",
reply_markup=keyboard,
parse_mode="HTML")


@dp.pre_checkout_query()
async def pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@dp.message(lambda message: message.successful_payment is not None)
async def successful_payment(message: types.Message):
    await message.answer("""
<tg-emoji emoji-id="5192879906295397710">💝</tg-emoji> Огромное спасибо за поддержку!
""",
parse_mode="HTML")


### ▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱ ###


@dp.message()
async def button_handler(message: types.Message) -> None:

    if message.text == "📋 Меню столовой на ближайший день":
        await message.reply_photo(photo=await menu(), caption=f"Меню известное на данный момент")


    elif message.text == "🗓 Расписание на любой день":
        await message.reply("Выбери день недели", reply_markup=button(["понедельник", "вторник", "среда", "четверг", "пятница"], 1))


    elif message.text == "⚙ Настройки":
        if str(await base_work(school_base, f"SELECT auto_send FROM user_data WHERE user_id='{message.chat.id}'"))[3:-4] == 'вкл':
            item1 = 'авто отправка  🔔'
        else:
            item1 = 'авто отправка  🔕'
        await message.reply("Настройки бота:", reply_markup=button([item1], 1))


    elif message.text == "👤 Профиль":
        await message.reply(f"""
<tg-emoji emoji-id="5231012545799666522">🔍</tg-emoji> <b>Твой профиль</b>
<b>──────────────────────</b>
<tg-emoji emoji-id="5271604874419647061">🔗</tg-emoji> <b>ID:</b> <code>{message.chat.id}</code>
      <b>Имя:</b> <code>{message.chat.first_name}</code>
<b>──────────────────────</b>
<tg-emoji emoji-id="5424818078833715060">📣</tg-emoji> <b>Авто отправка:</b> <code>{str(await base_work(school_base, f"SELECT auto_send FROM user_data WHERE user_id = '{message.chat.id}'"))[3:-4]}</code>
<b>──────────────────────</b>
_версия бота v1.2 beta_
""", parse_mode="HTML")


### ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡ ###


@dp.callback_query()
async def callback_button_handler(callback: CallbackQuery):
    if callback.data == 'понедельник':
        await callback.message.answer_photo(photo=await photo('monday'), caption=f"Расписание на понедельник")

    if callback.data == 'вторник':
        await callback.message.answer_photo(photo=await photo('tuesday'), caption=f"Расписание на вторник")

    if callback.data == 'среда':
        await callback.message.answer_photo(photo=await photo('wednesday'), caption=f"Расписание на среду")

    if callback.data == 'четверг':
        await callback.message.answer_photo(photo=await photo('thursday'), caption=f"Расписание на четверг")

    if callback.data == 'пятница':
        await callback.message.answer_photo(photo=await photo('friday'), caption=f"Расписание на пятницу")


### ▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱ ###

    if callback.data == 'авто отправка  🔔':

        await base_work(school_base,
                        f"UPDATE user_data SET auto_send = 'выкл' WHERE user_id = '{callback.message.chat.id}'")
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Настройки бота:",
            reply_markup=button(['авто отправка  🔕'], 1)
        )
        return


    if callback.data == 'авто отправка  🔕':

        await base_work(school_base,
                        f"UPDATE user_data SET auto_send = 'вкл' WHERE user_id = '{callback.message.chat.id}'")
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text="Настройки бота:",
            reply_markup=button(['авто отправка  🔔'], 1)
        )
        return


### ▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱ ###


async def main():

    await init_days()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_updates, "interval", seconds=60*45)
    scheduler.add_job(save_menu, "interval", seconds=60*30)
    scheduler.start()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
