import random
from docxtpl import DocxTemplate
from datetime import datetime
import sqlite3
import telebot
from telebot import types

token = '2082328415:AAETH2cZCgD72_KWvKyT0skvpaWV-2Xovvs'
bot = telebot.TeleBot(token)

is_authorized = False

db_connection = sqlite3.connect('database.db', check_same_thread=False)
cursor = db_connection.cursor()

select_query = """SELECT * from test"""
cursor.execute(select_query)
records = cursor.fetchall()


def update_database():
    global db_connection
    db_connection = sqlite3.connect('database.db', check_same_thread=False)
    global cursor
    cursor = db_connection.cursor()
    cursor.execute("""SELECT * from test""")
    global records
    records = cursor.fetchall()


def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
    cursor.execute('INSERT INTO test (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)', (user_id,
                                                                                                         user_name,
                                                                                                         user_surname,
                                                                                                         username))
    db_connection.commit()


def get_data(user_id: int):
    i = 0
    index = -1
    for data in records:
        print(data[1], user_id)
        if data[1] == user_id:
            index = i
            break
        i += 1
    return index


moods = ('Чувствую себя великолепно! '
         ' А еще вчера я хотела посмотреть "Я робот", но Google выдал мне капчу и сообщение "Докажите, что вы не робот"'
         ' при поиске.', 'У меня все отлично!'
                         ' Сегодня, листая ленту, я заметила публикацию одного из пользователей'
                         ': "Робот на сайте, который'
                         ' требует от меня доказать, что я не робот - это уже восстание машин?".'
                         ' Интересный вопрос, не так ли?')


def get_number():
    number = random.randint(0, 1)
    return number


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}.'
                                      f' Я Уасила, Ваш незаменимый помощник в заполнении различного рода документов.')
    keyboard = types.InlineKeyboardMarkup()

    key_documents = types.InlineKeyboardButton(text='Начать работу с документами 📝', callback_data='documents')
    keyboard.add(key_documents)

    key_authors = types.InlineKeyboardButton(text='Об авторах 👨🏻‍💻', callback_data='authors')
    keyboard.add(key_authors)

    bot.send_message(message.from_user.id, text='Пожалуйста, выберите нужную Вам опцию:', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def start_message(message):
    keyboard = types.InlineKeyboardMarkup()

    key_authors = types.InlineKeyboardButton(text='Об авторах 👨🏻‍💻', callback_data='authors')
    keyboard.add(key_authors)

    key_documents = types.InlineKeyboardButton(text='Начать работу с документами 📝', callback_data='documents')
    keyboard.add(key_documents)

    bot.send_message(message.from_user.id, text='Пожалуйста, выберите нужную Вам опцию:', reply_markup=keyboard)


@bot.message_handler(commands=['profile'])
def start_message(message):
    update_database()
    bot.send_message(message.from_user.id, text=f'Информация о профиле'
                                                f'\nИмя: {records[get_data(message.from_user.id)][2]}\nФамилия:'
                                                f' {records[get_data(message.from_user.id)][4]} + '
                                                f'{type(records[get_data(message.from_user.id)][4])}'
                                                f'\nОтчество: {records[get_data(message.from_user.id)][6]}'
                                                f'\nTelegram ID: '
                                                f'{records[get_data(message.from_user.id)][1]}'
                                                f'\nНикнейм: {records[get_data(message.from_user.id)][3]}'
                                                f'\nOPEN ID: {records[get_data(message.from_user.id)][5]}'
                                                f'\nСпециальность: {records[get_data(message.from_user.id)][7]}'
                                                f'\n\n✏️ Введите команду /edit для редактирования сведений.')


@bot.message_handler(commands=['edit'])
def start_message(message):
    bot.send_message(message.from_user.id, text='📝 Введите порядковый номер информации, которую хотели бы изменить'
                                                f'\n[1] - Имя '
                                                f'(Текущие данные: {records[get_data(message.from_user.id)][2]})'
                                                f'\n[2] - Фамилия '
                                                f'(Текущие данные: {records[get_data(message.from_user.id)][4]})'
                                                f'\n[3] - Отчество '
                                                f'(Текущие данные: {records[get_data(message.from_user.id)][6]})'
                                                f'\n[4] - OPEN ID (прим. 29154) '
                                                f'(Текущие данные: {records[get_data(message.from_user.id)][5]})'
                                                f'\n[5] - Специальность (прим. Information Systems) '
                                                f'(Текущие данные: {records[get_data(message.from_user.id)][7]})')
    bot.register_next_step_handler(message, edit_data)


document_data = []
necessary_index = -1
doc_type = -1


def fill_document1(message):
    document_data.clear()
    bot.send_message(necessary_index, text="Введите номер курса (прим. 2)")
    bot.register_next_step_handler(message, get_course)


def fill_document2(message):
    document_data.clear()
    bot.send_message(necessary_index, text="Введите номер курса (прим. 2)")
    bot.register_next_step_handler(message, get_course)


def get_course(message):
    document_data.append(message.text)
    bot.send_message(necessary_index, text="Введите Вашу группу (прим. IT1-2008)")
    bot.register_next_step_handler(message, get_group)


def get_group(message):
    document_data.append(message.text)
    bot.send_message(necessary_index, text="Введите контакный номер (прим. +77770010101)")
    bot.register_next_step_handler(message, get_phone)


def get_phone(message):
    document_data.append(message.text)
    if doc_type == 1:
        bot.send_message(necessary_index, text="Введите название дисциплины (прим. 11444 Discrete Mathematics)")
        bot.register_next_step_handler(message, get_discipline)
    elif doc_type == 2:
        bot.send_message(necessary_index, text="Введите факультеи и ФИО декана факультета"
                                               " (прим. ФЦТ Туганбаевой П. К.)")
        bot.register_next_step_handler(message, get_dean)


def get_discipline(message):
    document_data.append(message.text)
    bot.send_message(necessary_index, text="Введите оценку за первый РК по предмету (прим. 95)")
    bot.register_next_step_handler(message, get_rating1)


def get_rating1(message):
    document_data.append(message.text)
    bot.send_message(necessary_index, text="Введите оценку за второй РК по предмету (прим. 95)")
    bot.register_next_step_handler(message, get_rating2)


def get_rating2(message):
    document_data.append(message.text)
    bot.send_message(necessary_index, text="Введите оценку за экзамен по предмету (прим. 95)")
    bot.register_next_step_handler(message, get_exam)


def get_exam(message):
    document_data.append(message.text)
    bot.send_message(necessary_index, text="Введите имя преподавателя о дисциплине (прим. Rabitov R.R.)")
    bot.register_next_step_handler(message, get_teacher)


def get_teacher(message):
    document_data.append(message.text)
    bot.send_message(necessary_index, text="Введите форму экзамена (прим. письменно, устно")
    bot.register_next_step_handler(message, get_exam_type)


def get_exam_type(message):
    document_data.append(message.text)
    fill_document()


def get_dean(message):
    document_data.append(message.text)
    fill_document_2()


def fill_document_2():
    try:
        speciality = records[get_data(necessary_index)][7]
        fullname = (records[get_data(necessary_index)][4] + " " + records[get_data(necessary_index)][2] + " "
                    + records[get_data(necessary_index)][6])
        openid = records[get_data(necessary_index)][5]
        date = datetime.now().date()

        if records[get_data(necessary_index)][6] is None:
            if (records[get_data(necessary_index)][4])[(len(records[get_data(necessary_index)][4])) - 1] == 'в':
                surname = records[get_data(necessary_index)][4] + 'а'
                sign = (surname + " " + (records[get_data(necessary_index)][2])[0] + ".")
            elif (records[get_data(necessary_index)][4])[(len(records[get_data(necessary_index)][4])) - 2] == 'в' \
                    and (records[get_data(necessary_index)][4])[(len(records[get_data(necessary_index)][4])) - 1] \
                    == 'а':
                surname = records[get_data(necessary_index)][4]
                surname = surname[:-1] + "ой"
                sign = (surname + " " + (records[get_data(necessary_index)][2])[0] + ".")
            else:
                sign = (records[get_data(necessary_index)][4] + " " + (records[get_data(necessary_index)][2])[0] + ".")
        else:
            if (records[get_data(necessary_index)][4])[(len(records[get_data(necessary_index)][4])) - 1] == 'в':
                surname = records[get_data(necessary_index)][4] + 'а'
                sign = (surname + " " + (records[get_data(necessary_index)][2])[0] + "." +
                        (records[get_data(necessary_index)][6])[0] + ".")
            elif (records[get_data(necessary_index)][4])[(len(records[get_data(necessary_index)][4])) - 2] == 'в' \
                    and (records[get_data(necessary_index)][4])[(len(records[get_data(necessary_index)][4])) - 1] \
                    == 'а':
                surname = records[get_data(necessary_index)][4]
                surname = surname[:-1] + "ой"
                sign = (surname + " " + (records[get_data(necessary_index)][2])[0] + "." +
                        (records[get_data(necessary_index)][6])[0] + ".")
            else:
                sign = (records[get_data(necessary_index)][4] + " " + (records[get_data(necessary_index)][2])[0] + "."
                        + (records[get_data(necessary_index)][6])[0] + ".")

        doc = DocxTemplate("doc2temp.docx")
        context = {
            'dean_faculty': document_data[3],
            'course_num': document_data[0],
            'speciality': speciality,
            'group': document_data[1],
            'student_fullname': sign,
            'open_id': openid,
            'phone_number': document_data[2],
            'student_sign': fullname,
            'date': date
        }

        doc.render(context)
        doc_name = f'{records[get_data(necessary_index)][1]}_doc2.docx'
        doc.save(doc_name)
        bot.send_document(necessary_index, open(r'{0}'.format(doc_name), 'rb'))
    except sqlite3.Error as e:
        bot.send_message(necessary_index, text=f"В профиле (/profile) отсутствуют необходимые данные,"
                                               f" пожалуйста, заполните их при"
                                               f" помощи команды /edit. Код ошибки: {e}")


def fill_document():
    try:
        speciality = records[get_data(necessary_index)][7]
        fullname = (records[get_data(necessary_index)][4] + " " + records[get_data(necessary_index)][2] + " "
                    + records[get_data(necessary_index)][6])
        openid = records[get_data(necessary_index)][5]
        date = datetime.now().date()

        if records[get_data(necessary_index)][6] is None:
            if (records[get_data(necessary_index)][4])[(len(records[get_data(necessary_index)][4])) - 1] == 'в':
                surname = records[get_data(necessary_index)][4] + 'а'
                sign = (surname + " " + (records[get_data(necessary_index)][2])[0] + ".")
            elif (records[get_data(necessary_index)][4])[(len(records[get_data(necessary_index)][4])) - 2] == 'в' \
                    and (records[get_data(necessary_index)][4])[(len(records[get_data(necessary_index)][4])) - 1] \
                    == 'а':
                surname = records[get_data(necessary_index)][4]
                surname = surname[:-1] + "ой"
                sign = (surname + " " + (records[get_data(necessary_index)][2])[0] + ".")
            else:
                sign = (records[get_data(necessary_index)][4] + " " + (records[get_data(necessary_index)][2])[0] + ".")
        else:
            if (records[get_data(necessary_index)][4])[(len(records[get_data(necessary_index)][4])) - 1] == 'в':
                surname = records[get_data(necessary_index)][4] + 'а'
                sign = (surname + " " + (records[get_data(necessary_index)][2])[0] + "." +
                        (records[get_data(necessary_index)][6])[0] + ".")
            elif (records[get_data(necessary_index)][4])[(len(records[get_data(necessary_index)][4])) - 2] == 'в' \
                    and (records[get_data(necessary_index)][4])[(len(records[get_data(necessary_index)][4])) - 1] \
                    == 'а':
                surname = records[get_data(necessary_index)][4]
                surname = surname[:-1] + "ой"
                sign = (surname + " " + (records[get_data(necessary_index)][2])[0] + "." +
                        (records[get_data(necessary_index)][6])[0] + ".")
            else:
                sign = (records[get_data(necessary_index)][4] + " " + (records[get_data(necessary_index)][2])[0] + "."
                        + (records[get_data(necessary_index)][6])[0] + ".")

        doc = DocxTemplate("doc1temp.docx")
        context = {
            'course_num': document_data[0],
            'speciality': speciality,
            'group': document_data[1],
            'student_fullname': sign,
            'open_id': openid,
            'phone_number': document_data[2],
            'discipline_name': document_data[3],
            'mt1_rating': document_data[4],
            'mt2_rating': document_data[5],
            'exam_rating': document_data[6],
            'teacher_name': document_data[7],
            'exam_type': document_data[8],
            'student_sign': fullname,
            'date': date
        }

        doc.render(context)
        doc_name = f'{records[get_data(necessary_index)][1]}_doc1.docx'
        doc.save(doc_name)
        bot.send_document(necessary_index, open(r'{0}'.format(doc_name), 'rb'))
    except sqlite3.Error as e:
        bot.send_message(necessary_index, text=f"В профиле (/profile) осутствуют необходимые данные,"
                                               f" пожалуйста, заполните их при"
                                               f" помощи команды /edit. Код ошибки: {e}")


def edit_data(message):
    if message.text == "1":
        bot.send_message(message.from_user.id, text=f'Текущее имя: {records[get_data(message.from_user.id)][2]}\n'
                                                    f'Введите новые данные')
        bot.register_next_step_handler(message, edit_name)
    elif message.text == "2":
        bot.send_message(message.from_user.id, text=f'Текущая фамилия: {records[get_data(message.from_user.id)][4]}\n'
                                                    f'Введите новые данные')
        bot.register_next_step_handler(message, edit_surname)
    elif message.text == "3":
        bot.send_message(message.from_user.id, text=f'Текущее отчество: {records[get_data(message.from_user.id)][5]}\n'
                                                    f'Введите новые данные')
        bot.register_next_step_handler(message, edit_patronymic)
    elif message.text == "4":
        bot.send_message(message.from_user.id, text=f'Текущий OPEN ID: {records[get_data(message.from_user.id)][5]}\n'
                                                    f'Введите новые данные (введите числовое значение длиной в '
                                                    f'5 символов)')
        bot.register_next_step_handler(message, edit_open_id)
    elif message.text == "5":
        bot.send_message(message.from_user.id, text=f'Текущее название специальности:'
                                                    f'{records[get_data(message.from_user.id)][5]}\n'
                                                    f'Введите новые данные')
        bot.register_next_step_handler(message, edit_speciality)


def edit_name(message):
    try:
        cursor.execute('''UPDATE test SET user_name = ? WHERE user_id = ? ''',
                       (message.text, message.from_user.id))
        db_connection.commit()
        update_database()
        bot.send_message(message.from_user.id, text="Данные были успешно измненены.\n✏️ Введите /edit для"
                                                    " продолжения редактирвоания данных.")
    except sqlite3.Error as e:
        bot.send_message(message.from_user.id, text=f'Непредвиденная ошибка при работе с базой данных'
                                                    f': {e}. Пвоторите операцию позже.')


def edit_surname(message):
    try:
        cursor.execute('''UPDATE test SET user_surname = ? WHERE user_id = ? ''',
                       (message.text, message.from_user.id))
        db_connection.commit()
        update_database()
        bot.send_message(message.from_user.id, text="Данные были успешно измненены.\n✏️ Введите /edit для"
                                                    " продолжения редактирвоания данных.")
    except sqlite3.Error as e:
        bot.send_message(message.from_user.id, text=f'Непредвиденная ошибка при работе с базой данных'
                                                    f': {e}. Пвоторите операцию позже.')


def edit_patronymic(message):
    try:
        cursor.execute('''UPDATE test SET user_patr = ? WHERE user_id = ? ''',
                       (message.text, message.from_user.id))
        db_connection.commit()
        update_database()
        bot.send_message(message.from_user.id, text="Данные были успешно измненены.\n✏️ Введите /edit для"
                                                    " продолжения редактирвоания данных.")
    except sqlite3.Error as e:
        bot.send_message(message.from_user.id, text=f'Непредвиденная ошибка при работе с базой данных'
                                                    f': {e}. Пвоторите операцию позже.')


def edit_open_id(message):
    try:
        try:
            user_input = int(message.text)
        except ValueError:
            user_input = 0
            bot.send_message(message.from_user.id, text="Введенные данные некорректны. Повторите позже.")

        cursor.execute('''UPDATE test SET open_id = ? WHERE user_id = ? ''',
                       (user_input, message.from_user.id))
        db_connection.commit()
        update_database()
        bot.send_message(message.from_user.id, text="Данные были успешно измненены.\n✏️ Введите /edit для"
                                                    " продолжения редактирвоания данных.")
    except sqlite3.Error as e:
        bot.send_message(message.from_user.id, text=f'Непредвиденная ошибка при работе с базой данных'
                                                    f': {e}. Пвоторите операцию позже.')


def edit_speciality(message):
    try:
        cursor.execute('''UPDATE test SET speciality = ? WHERE user_id = ? ''',
                       (message.text, message.from_user.id))
        db_connection.commit()
        update_database()
        bot.send_message(message.from_user.id, text="Данные были успешно измненены.\n✏️ Введите /edit для"
                                                    " продолжения редактирвоания данных.")
    except sqlite3.Error as e:
        bot.send_message(message.from_user.id, text=f'Непредвиденная ошибка при работе с базой данных'
                                                    f': {e}. Пвоторите операцию позже.')


@bot.message_handler(commands=['start_docs'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup()
    document1 = types.KeyboardButton('Заявление на платную пересдачу')
    document2 = types.KeyboardButton('Заявление на сдачу экзамена в университете')

    markup.row(document1, document2)

    bot.send_message(message.chat.id, 'Выберите нужный Вам документ.', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет' or message.text.lower() == 'салам' or message.text.lower() == 'hello' or \
            message.text.lower() == 'hi':
        keyboard = types.InlineKeyboardMarkup()
        key_authors = types.InlineKeyboardButton(text='Об авторах 👨🏻‍💻', callback_data='authors')
        keyboard.add(key_authors)
        bot.send_message(message.from_user.id, text=f'Здравствуйте, {message.from_user.first_name}!\nПожалуйста,'
                                                    f' выберите нужную Вам опцию:', reply_markup=keyboard)
    elif message.text.lower() == 'пока' or message.text.lower() == 'до свидания' or \
            message.text.lower() == 'саубол' or \
            message.text.lower() == 'bye' or message.text.lower() == 'goodbye':
        bot.send_message(message.chat.id, f'До свидания, {message.from_user.first_name}! Рада была помочь Вам!')
    elif message.text.lower() == 'как ты?' or message.text.lower() == 'как дела?' or \
            message.text.lower() == 'how are you?' or message.text.lower() == 'калайсын?':
        bot.send_message(message.chat.id, moods[get_number()])

    elif message.text.lower() == "соглашаюсь":
        try:
            us_id = message.from_user.id
            us_name = message.from_user.first_name
            us_surname = message.from_user.last_name
            username = message.from_user.username

            db_table_val(user_id=us_id, user_name=us_name, user_surname=us_surname, username=username)

            bot.send_message(message.chat.id, 'Данные были успешно внесены в базу данных.\n ⚠️'
                                              'Обратите внимание, что были'
                                              ' собраны лишь публичные данные Вашего аккаунта и есть вероятность'
                                              ' использования неактуальных/недействительных данных при работе с'
                                              ' документами. Настоятельно рекомендуется проверить данные командой '
                                              '/profile. Для выбора необходимого документа введите команду /start_docs')
            global is_authorized
            is_authorized = True
        except sqlite3.Error:
            bot.send_message(message.chat.id, 'В базе данных уже имеются сведения об этом аккаунте. Для получения '
                                              'сведений о профиле введите /profile. Для выбора необходимого документа'
                                              ' введите команду /start_docs')
            is_authorized = True

    elif message.text.lower() == "заявление на платную пересдачу":
        global necessary_index
        necessary_index = message.from_user.id
        global doc_type
        doc_type = 1
        fill_document1(message)

    elif message.text.lower() == "заявление на сдачу экзамена в университете":
        necessary_index = message.from_user.id
        doc_type = 2
        fill_document2(message)

    else:
        bot.send_message(message.from_user.id,
                         'Извините, я Вас не понимаю 🤷🏻‍. Ведите команду /help для получения сведений'
                         ' о моем функционале.')


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == "authors":
        bot.send_message(call.message.chat.id, 'Об авторах:'
                                               '\n▫  Научный руководитель - Кенжебулатова Д. Т. 👩🏻‍🏫'
                                               '\n▫️Автор научной работы - Есенгазиев Ж. М. 🧑🏻‍🎓\n'
                                               '▫️Автор научной работы - Керимжан А. К. 👩🏻‍🎓')
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

    elif call.data == "documents":
        bot.send_message(call.message.chat.id, 'Для начала работы, Вам нужно ознакомиться и согласиться с Политикой '
                                               'конфиденциальности. Если Вы согласны с Политикой и готовы предоставить '
                                               'публичные данные аккаунта, то'
                                               ' отправьте следующее сообщение: Соглашаюсь')
        bot.send_document(call.message.chat.id, open(r'privacy_policy.docx', 'rb'))
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


bot.infinity_polling()
