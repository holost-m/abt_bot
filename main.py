import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, FSInputFile, Message
from aiogram.filters.command import Command
from tg_token import TOKEN

from aiogram import F
import redis
from db_connect import *

import datetime
import os

# Подключаем redis
r = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)
r.flushdb() # полностью все удаляем

# полностью удаляем информацию из бд
# drop_all_info_db()

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=TOKEN)
# Диспетчер
dp = Dispatcher()

# Служебные функции

password_admin = 'Green90'

def tg_id_by_message(message):
    return message.from_user.id

def today_str():
    return datetime.datetime.now().date().isoformat()

def is_isoformat_date(date_day):
    try:
        datetime.date.fromisoformat(date_day)
    except:
        return False
    return True

def get_all_marks_by_tg_id(tg_id, abt=True):
    id = Children.get_id_by_tg_id(tg_id)

    res = Children_marks.my_marks(int(id))

    dct = {}
    sum1 = 0
    if abt:
        sum1 = 1

    if res:
        res = list(map(lambda x: x[0], res))

        for i in res:
            sum1 += 1
            if i in dct:
                dct[i] += 1
            else:
                dct[i] = 1
    if len(dct) == 5:
        dct['ЗОЛОТАЯ ЗВЕЗДА⭐'] = 1
        sum1 += 1
    if abt:
        dct['АБТ'] = 1
    result = '\n' + '\n'.join(list(map(lambda x: f'{x[0]} : {x[1]}', dct.items()))) + f'\nВсего значков: {sum1}'
    return [result, sum1]




# Клавиатура
kb_list1 = [
        [KeyboardButton(text="Участник💥")],
        [KeyboardButton(text="Организатор💫")]
    ]
keyboard1 = ReplyKeyboardMarkup(keyboard=kb_list1, resize_keyboard=True, one_time_keyboard=True)

kb_list2 = [
        [KeyboardButton(text="Описание значков📒")],
        [KeyboardButton(text="Мои значки📈")],
        [KeyboardButton(text="Расписание📅")],
        [KeyboardButton(text="Информация на сегодня📌")],
    ]
keyboard_menu = ReplyKeyboardMarkup(keyboard=kb_list2, resize_keyboard=True, one_time_keyboard=True)

kb_list3 = [
        [KeyboardButton(text="Вожатый")],
        [KeyboardButton(text="Член ОК")],
        [KeyboardButton(text="Руководство смены")]
    ]
keyboard_admin_level = ReplyKeyboardMarkup(keyboard=kb_list3, resize_keyboard=True, one_time_keyboard=True)

kb_list4 = [
        [KeyboardButton(text="Расписание на сегодня🕘")],
        [KeyboardButton(text="Вручить значок📈")],
        [KeyboardButton(text="Добавить описание дня📌")],
        [KeyboardButton(text="Добавить расписание📅")],
        [KeyboardButton(text="Посмотреть статистику значков📊")]
    ]
keyboard_admin_menu2 = ReplyKeyboardMarkup(keyboard=kb_list4, resize_keyboard=True, one_time_keyboard=True)

kb_list6 = [
        [KeyboardButton(text="Назад👈")],
        [KeyboardButton(text="№ 1")],
        [KeyboardButton(text="№ 2")],
        [KeyboardButton(text="№ 3")],
        [KeyboardButton(text="№ 4")],
        [KeyboardButton(text="№ 5")]
    ]
keyboard_groups = ReplyKeyboardMarkup(keyboard=kb_list6, resize_keyboard=True, one_time_keyboard=True)

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    tg_id = tg_id_by_message(message)
    if tg_id not in Children.get_all_tg_id() and str(tg_id) not in r.keys():
        r.set(str(tg_id), '100')
        await message.answer('''Приветсвуем тебя, участник смены АБТ 2024! В этом боте ты сможешь получить информацию о сегодняшнем дне, а также узнать какие значки тебе удалось собрать. Но сначала тебе необходимо пройти регистрацию''')
        await message.answer('Выберите Вашу роль:', reply_markup=keyboard1)

@dp.message(F.text=="Описание значков📒")
async def echo_menu1(message: types.Message):
    tg_id = tg_id_by_message(message)
    if r.get(str(tg_id)) == '106':
        kb_list5 = []
        lst_db = Marks.get_all_marks_name()
        rs = list(map(lambda x: x[0], Marks.get_all_marks_name()))
        for name in rs:
            kb_list5.append([KeyboardButton(text=name)])
        keyboard_marks = ReplyKeyboardMarkup(keyboard=kb_list5, resize_keyboard=True, one_time_keyboard=True)
        await message.answer('Выберите значок:', reply_markup=keyboard_marks)
        r.set(str(tg_id), '107')


@dp.message(F.text=="Мои значки📈")
async def echo_menu2(message: types.Message):
    tg_id = tg_id_by_message(message)
    if r.get(str(tg_id)) == '106':
        result = get_all_marks_by_tg_id(tg_id)[0]

        await message.answer(result)
        await message.answer('Выберите действие', reply_markup=keyboard_menu)
    else:
        await message.answer('Значки в разработке')
        await message.answer('Выберите действие', reply_markup=keyboard_menu)

@dp.message(F.text=="Расписание📅")
async def echo_menu3(message: types.Message):
    tg_id = tg_id_by_message(message)
    if r.get(str(tg_id)) == '106':
        timetable_path = f'timetable_photo/{today_str()}.png'
        if os.path.exists(timetable_path):
            photo = FSInputFile(timetable_path)
            await message.answer_photo(photo=photo, caption="Расписание на сегодня")
            await message.answer('Выберите действие', reply_markup=keyboard_menu)
        else:
            await message.answer('Расписание на сегодня загружается')
            await message.answer('Выберите действие', reply_markup=keyboard_menu)



@dp.message(F.text=="Информация на сегодня📌")
async def echo_menu4(message: types.Message):
    tg_id = tg_id_by_message(message)
    if r.get(str(tg_id)) == '106':
        res = Dayinfo.get_dayinfo_by_day(today_str())
        if res:
            res = res[2]

        else:
            res = 'Информация по дню в разработке'
        await message.answer(res)
        await message.answer('Выберите действие', reply_markup=keyboard_menu)





# Меню руководства смены
@dp.message(F.text=="Добавить описание дня📌")
async def echo_menu5(message: types.Message):
    tg_id = tg_id_by_message(message)
    if r.get(str(tg_id)) == '206':
        r.set(str(tg_id), '310')
        await message.answer('Приложите описание на сегодня в формате текста')

@dp.message(F.text=="Добавить расписание📅")
async def echo_menu6(message: types.Message):
    tg_id = tg_id_by_message(message)
    if r.get(str(tg_id)) == '206':
        r.set(str(tg_id), '320')
        await message.answer('Введите дату в формате ГГГГ-MM-ДД:')

@dp.message(F.text=="Добавить значок📒")
async def echo_menu6(message: types.Message):
    tg_id = tg_id_by_message(message)
    if r.get(str(tg_id)) == '206':
        r.set(str(tg_id), '330')
        await message.answer('Введите название значка:')

@dp.message(F.text=="Вручить значок📈")
async def echo_menu6(message: types.Message):
    tg_id = tg_id_by_message(message)
    if r.get(str(tg_id)) == '206':
        admin_id = Admins.get_id_by_tg_id(tg_id)
        if Children_marks.count_of_marks(admin_id, today_str()) <= 5:
            await message.answer('Выберите отряд:', reply_markup=keyboard_groups)
            r.set(str(tg_id), '340')
        else:
            r.set(str(tg_id), '206')
            await message.answer('Лимит значков на сегодня исчерпан. Спасибо за активность!')
            await message.answer('Выберите действие', reply_markup=keyboard_admin_menu2)
    else:
        await message.answer('Нажмите любую клавишу')

@dp.message(F.text=="Посмотреть статистику значков📊")
async def echo_menu7(message: types.Message):
    tg_id = tg_id_by_message(message)
    if r.get(str(tg_id)) == '206':

        result = []
        for tg_id in Children.get_all_tg_id():

            name_lastname_lst = ' '.join(Children.get_name_lastname_by_tg_id(tg_id))
            lst = get_all_marks_by_tg_id(tg_id, False)
            lst.append(name_lastname_lst)
            result.append(lst)



        result1 = sorted(result, key=lambda x: -x[1])[:40]
        result1 = '\n'.join([i[2] + i[0] + '\n' for i in result1])
        await message.answer(result1)

        result2 = sorted(result, key=lambda x: -x[1])[40:]
        result2 = '\n'.join([i[2] + i[0] + '\n' for i in result2])
        await message.answer(result2)

        await message.answer('Выберите действие', reply_markup=keyboard_admin_menu2)

@dp.message(F.text=="Расписание на сегодня🕘")
async def echo_menu8(message: types.Message):
    tg_id = tg_id_by_message(message)
    if r.get(str(tg_id)) == '206':
        timetable_path = f'timetable_photo/{today_str()}.png'
        if os.path.exists(timetable_path):
            photo = FSInputFile(timetable_path)
            await message.answer_photo(photo=photo, caption="Расписание на сегодня")
            await message.answer('Выберите действие', reply_markup=keyboard_admin_menu2)
        else:
            await message.answer('Расписание на сегодня загружается')
            await message.answer('Выберите действие', reply_markup=keyboard_admin_menu2)


@dp.message()
async def echo_message(message: types.Message):

    tg_id = tg_id_by_message(message)
    f1 = tg_id in Children.get_all_tg_id()
    f2 = tg_id in Admins.get_all_tg_id()
    f3 = str(tg_id) in r.keys()

    if not (f1 or f2 or f3):
        r.set(str(tg_id), '100')
        await message.answer(
            '''Приветствуем тебя, участник смены АБТ 2024! В этом боте ты сможешь получить информацию о сегодняшнем дне, а также узнать какие значки тебе удалось собрать. Но сначала тебе необходимо пройти регистрацию''')
        await message.answer('Выберите Вашу роль:', reply_markup=keyboard1)


    elif r.get(str(tg_id)) == '100':
        if message.text == "Участник💥":
            r.set(str(tg_id), '102')  # установили состояние
            await message.answer('Введите Ваше имя:')

        elif message.text == "Организатор💫":
            r.set(str(tg_id), '202')  # установили состояние
            await message.answer('Введите пароль:')
        else:
            await message.answer('Выберите Вашу роль:', reply_markup=keyboard1)


    elif r.get(str(tg_id)) == '102':
        r.set(str(tg_id), '103') # установили состояние

        reg_tg_id = f'reg:{tg_id}' # получили имя переменной reg:1212938421
        r.lpush(reg_tg_id, message.text.replace(' ', '')) # создали список


        await message.answer('Введите Вашу фамилию:')

    elif r.get(str(tg_id)) == '103':
        r.set(str(tg_id), '104') # установили состояние

        reg_tg_id = f'reg:{tg_id}' # получили имя переменной reg:1212938421
        r.rpush(reg_tg_id, message.text.replace(' ', '')) # добавили фамилию в список


        await message.answer('Введите Ваш возраст числом:')

    elif r.get(str(tg_id)) == '104':

        try:
            int(message.text)
            r.set(str(tg_id), '105')  # установили состояние

            reg_tg_id = f'reg:{tg_id}'  # получили имя переменной reg:1212938421
            r.rpush(reg_tg_id, message.text)  # добавили возраст в список


            await message.answer('Введите № вашего отряда числом:')
        except:
            await message.answer('Введите Ваш возраст ЧИСЛОМ:')


    elif r.get(str(tg_id)) == '105':

        try:
            int(message.text)
            if int(message.text) in (1, 2, 3, 4, 5):
                r.set(str(tg_id), '106') # установили состояние

                reg_tg_id = f'reg:{tg_id}' # получили имя переменной reg:1212938421
                r.rpush(reg_tg_id, message.text) # добавили отряд в список
            else:
                raise Exception
        except:
            await message.answer('Введите № вашего отряда ЧИСЛОМ:')
        # запишем участника в бд

        lst = r.lrange(reg_tg_id, 0, -1)
        child_info = [tg_id, lst[0], lst[1], int(lst[2]), int(lst[3])]
        res = Children.add_children(*child_info)
        if res:
            await message.answer('Регистрация завершена')

        await message.answer('Выберите действие', reply_markup=keyboard_menu)

    elif r.get(str(tg_id)) == '106':

        await message.answer('Выберите действие', reply_markup=keyboard_menu)

    elif r.get(str(tg_id)) == '202':
        step = message.text
        if step == password_admin:
            r.set(str(tg_id), '203')
            await message.answer('Введите Ваше имя:')
        else:
            r.set(str(tg_id), '100')
            await message.answer('Неверный пароль. Выберите Вашу роль:', reply_markup=keyboard1)

    elif r.get(str(tg_id)) == '203':
        r.set(str(tg_id), '204')  # установили состояние

        reg_tg_id = f'reg:{tg_id}'  # получили имя переменной reg:1212938421
        r.lpush(reg_tg_id, message.text.replace(' ', ''))  # создали список



        await message.answer('Введите Вашу фамилию:')


    elif r.get(str(tg_id)) == '204':
        r.set(str(tg_id), '205') # установили состояние

        reg_tg_id = f'reg:{tg_id}' # получили имя переменной reg:1212938421
        r.rpush(reg_tg_id, message.text.replace(' ', '')) # добавили фамилию в список


        await message.answer('Выберите Вашу роль в ОК:', reply_markup=keyboard_admin_level)

    elif r.get(str(tg_id)) == '205':
        dct = {'Вожатый': 2, 'Член ОК': 2, 'Руководство смены': 1}
        if message.text in dct:

            res = dct.get(message.text)

            r.set(str(tg_id), '206')  # установили состояние
            reg_tg_id = f'reg:{tg_id}'  # получили имя переменной reg:1212938421
            r.rpush(reg_tg_id, res)  # добавили уровень в список

            # запишем админа в бд

            lst = r.lrange(reg_tg_id, 0, -1)
            admin_info = [tg_id, lst[0], lst[1], res]
            if tg_id == 762151919:
                admin_info.append(1)
            res2 = Admins.add_admin(*admin_info)
            await message.answer('Регистрация завершена')
            await message.answer('Выберите действие', reply_markup=keyboard_admin_menu2)

        else:
            await message.answer('Выберите Вашу роль в ОК:', reply_markup=keyboard_admin_level)

    elif r.get(str(tg_id)) == '206':
        await message.answer('Выберите действие', reply_markup=keyboard_admin_menu2)

    # Добавляем инфу по дню
    elif r.get(str(tg_id)) == '310':
        info = message.text
        date_day = today_str()
        Dayinfo.delete_day(date_day)

        Dayinfo.add_dayinfo(date_day, info)
        r.set(str(tg_id), '206')
        await message.answer('Выберите действие', reply_markup=keyboard_admin_menu2)


    # Добавляем расписание
    elif r.get(str(tg_id)) == '320':

        date_day = message.text
        if is_isoformat_date(date_day):
            timetable_tg_id = f'timetable:{tg_id}'  # получили имя переменной reg:1212938421
            r.set(timetable_tg_id, date_day)  # создали список
            r.set(str(tg_id), '321')
            await message.answer('Загрузите фото расписания в формате png')
        else:
            await message.answer('Неверный формат даты')
            r.set(str(tg_id), '206')
            await message.answer('Выберите действие', reply_markup=keyboard_admin_menu2)

    elif r.get(str(tg_id)) == '321':
        timetable_tg_id = f'timetable:{tg_id}'
        date_timetable = r.get(timetable_tg_id)
        timetable_path = f'timetable_photo/{date_timetable}.png'
        if os.path.exists(timetable_path):
            os.remove(timetable_path)
        if message.photo:
            await message.bot.download(file=message.photo[-1].file_id, destination=timetable_path)
            r.set(str(tg_id), '206')
            await message.answer('Фото сохранено')
            await message.answer('Выберите действие', reply_markup=keyboard_admin_menu2)
        else:
            r.set(str(tg_id), '206')
            await message.answer('Неверный формат')
            await message.answer('Выберите действие', reply_markup=keyboard_admin_menu2)


    # Значки
    elif r.get(str(tg_id)) == '330':
        name = message.text
        mark_key = f'mark:{tg_id}'
        r.set(str(tg_id), '331')
        r.set(mark_key, name)
        await message.answer('Введите текстовое описание значка')

    elif r.get(str(tg_id)) == '331':
        desc = message.text
        mark_key = f'mark:{tg_id}'
        mark_name = r.get(mark_key)
        mark_name_and_desc = mark_name + '@@@' + desc

        r.set(mark_key, mark_name_and_desc)
        r.set(str(tg_id), '332')

        await message.answer('Загрузите фото значка')



    elif r.get(str(tg_id)) == '332':
        mark_key = f'mark:{tg_id}'
        res_db = r.get(mark_key).split('@@@')
        mark_path = f'marks_photo/{res_db[0]}.jpg'
        if os.path.exists(mark_path):
            os.remove(mark_path)

        if message.photo:
            await message.bot.download(file=message.photo[-1].file_id, destination=mark_path )
            r.set(str(tg_id), '206')

            Marks.add_mark(res_db[0], res_db[1], res_db[0] + '.jpg')

            await message.answer('Значок сохранен')
            await message.answer('Выберите действие', reply_markup=keyboard_admin_menu2)
        else:
            await message.answer('Неверный формат фото')

        r.set(str(tg_id), '206')
        await message.answer('Выберите действие', reply_markup=keyboard_admin_menu2)

    elif r.get(str(tg_id)) == '340':
        if message.text == "Назад👈":
            r.set(str(tg_id), '206')
            await message.answer('Выберите действие', reply_markup=keyboard_admin_menu2)

        else:
            group = message.text[-1]

            сhildren = Children.get_children_by_group(group)
            if сhildren:
                kb_list7 = []
                kb_list7.append([KeyboardButton(text=f'Назад👈')])
                for i in сhildren:
                    kb_list7.append([KeyboardButton(text=f'{i[2]} {i[3]}')])

                keyboard_group = ReplyKeyboardMarkup(keyboard=kb_list7, resize_keyboard=True, one_time_keyboard=True)
                await message.answer('Выберите участника', reply_markup=keyboard_group)
                r.set(str(tg_id), '341')



            else:

                r.set(str(tg_id), '206')
                await message.answer('Выберите действие', reply_markup=keyboard_admin_menu2)

    elif r.get(str(tg_id)) == '341':
        if message.text == 'Назад👈':
            r.set(str(tg_id), '206')
            await message.answer('Выберите действие', reply_markup=keyboard_admin_menu2)
        else:
            get_mark_tg_id = f'get_mark:{tg_id}'  # получили имя переменной get_mark:1212938421
            name_lastname = message.text.split()
            r.lpush(get_mark_tg_id, name_lastname[0])  # создали список
            r.rpush(get_mark_tg_id, name_lastname[1])  # добавили фамилию


            kb_list5 = []
            kb_list5.append([KeyboardButton(text=f'Назад👈')])
            lst_db = Marks.get_all_marks_name()

            rs = list(map(lambda x: x[0], Marks.get_all_marks_name()))
            rs.remove('АБТ')
            rs.remove('Золотая звезда')
            for name in rs:
                kb_list5.append([KeyboardButton(text=name)])

            keyboard_marks = ReplyKeyboardMarkup(keyboard=kb_list5, resize_keyboard=True, one_time_keyboard=True)
            r.set(str(tg_id), '342')
            await message.answer('Выберите значок:', reply_markup=keyboard_marks)

    elif r.get(str(tg_id)) == '342':
        if message.text == 'Назад👈':
            r.set(str(tg_id), '206')
            await message.answer('Выберите действие', reply_markup=keyboard_admin_menu2)
        else:
            get_mark_tg_id = f'get_mark:{tg_id}'
            lst = r.lrange(get_mark_tg_id, 0, -1)

            children_id = Children.get_id_by_name(lst[0], lst[1])
            marks_id = Marks.get_id_by_name(message.text)
            admin_id = Admins.get_id_by_tg_id(tg_id)

            Children_marks.add_mark(children_id, marks_id, today_str(), admin_id)

            # сообщаем пользователю
            children_tg_id = Children.get_tg_id_by_id(children_id)
            admin_name_last_name = ' '.join(Admins.get_name_lastname_by_id(admin_id))
            await bot.send_message(children_tg_id, f'Поздравляем! {admin_name_last_name} вручил Вам значок "{message.text}"')

            r.delete(get_mark_tg_id)

            r.set(str(tg_id), '206')
            await message.answer('Выберите действие', reply_markup=keyboard_admin_menu2)







    elif r.get(str(tg_id)) == '107':
        name = message.text
        mark_info = Marks.get_one_mark(name)

        if mark_info:

            if os.path.exists(f'marks_photo/{mark_info[3]}'):
                photo = FSInputFile(f'marks_photo/{mark_info[3]}')
                await message.answer_photo(photo=photo, caption=mark_info[2])
        else:
            await message.answer('Описание в разработке')
        r.set(str(tg_id), '106')
        await message.answer('Выберите действие', reply_markup=keyboard_menu)









        # нет в редис, есть в базе
    elif tg_id in Children.get_all_tg_id() and str(tg_id) not in r.keys():
        r.set(str(tg_id), '106')
        await message.answer('Выберите действие', reply_markup=keyboard_menu)

    # нет в редис, есть в базе
    elif tg_id in Admins.get_all_tg_id() and str(tg_id) not in r.keys():
        r.set(str(tg_id), '206')
        await message.answer('Выберите действие', reply_markup=keyboard_admin_menu2)




# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
