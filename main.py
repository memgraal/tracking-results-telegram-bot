from threading import Thread # этот можуль нужен только в случае, если мы собираемся добавлять отправку сообшений с определенныой переодичностью
from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, Document
from Config import TEACHER_CHAT_ID, BOT_TOKEN
import pandas as pd
import requests
from time import sleep

bot = TeleBot(token = BOT_TOKEN)


                                    # функции для реализации сообщений учителю о учениках, которые имею низкие показатели успеваемост
def SendResultsMessage(self) -> list[tuple]:
    Arr_of_users_negative_results = []

    DataFrame = pd.DataFrame(pd.read_excel("/curr_CSV_file/data.xlsx")) 
    
    for index, row in DataFrame.iterrows():
        #
        # Функциионал для выявления этих пользователей(подумаю, может использовать не цикл, а условие в самом pandas)
        # и запись их в Arr_of_users_negative_results в виде (имя, фамилия, группа, результаты)
        pass    
    return Arr_of_users_negative_results

def Send_Students_info_to_teacher():
    while True:
        # Отправляем сообщение
        All_results = SendResultsMessage()
        for x in All_results:
            for x1, x2, x3, x4 in x:
                url_req = "https://api.telegram.org/bot" + f"{BOT_TOKEN}" + "/sendMessage" + "?chat_id=" + f"{TEACHER_CHAT_ID}" + "&text=" + f"Сюда прописать напоминания и текущую статистику"
                requests.get(url_req)
        
        # ждем 3 дня до следующего сообщения 
        sleep(259200)

# Запускаем поток для отправки сообщений
# message_thread = Thread(target = Send_Students_info_to_teacher)
# message_thread.start()




# Команда /start
@bot.message_handler(commands=['start', 'hello'])
def start(message: Message) -> None:
    if str(message.chat.id) == TEACHER_CHAT_ID:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        replace_CSV = "Заменить текущий csv лист"
        show_unsatisfactory_students_results = "показать сниженные результаты учеников"

        markup.add(replace_CSV, show_unsatisfactory_students_results)
        
        bot.send_message(message.chat.id, text = f"Здравствуйте, {message.from_user.first_name}😀", reply_markup = markup)
        return 
    
    markup = ReplyKeyboardMarkup()
    StudentStats = "Показать мою статистику"
    markup.add(StudentStats)
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name} этот бот показывает твою статистику на Max.Edu.", reply_markup = markup)





# Обработка сообщений с документами
@bot.message_handler(content_types=['document'])
def handle_document(message: Message) -> None:
    if str(message.chat.id) == TEACHER_CHAT_ID:
        if message.document.file_name.endswith('.csv'):
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            try:
                with open('data.csv', 'wb') as f:
                    f.write(downloaded_file)

                new_dataFrame = pd.read_csv('data.csv')
                with pd.ExcelWriter('curr_CSV_file/data.xlsx') as new_excel:
                    new_dataFrame.to_excel(new_excel, index=False)

                bot.send_message(message.chat.id, "Файл успешно загружен")

            except Exception as e:
                bot.send_message(message.chat.id, f"Произошла ошибка: {e}")
        else:
            bot.send_message(message.chat.id, "Вы отправили не CSV-файл.")

        # возобновление вожможности пользоваться ReplyKeyboardMarkup
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        replace_CSV = "Заменить текущий csv лист"
        show_unsatisfactory_students_results = "показать сниженные результаты учеников"
        markup.add(replace_CSV, show_unsatisfactory_students_results)

        bot.send_message(message.chat.id, "💥", reply_markup = markup)
        
        
    else:
        bot.send_message(message.chat.id, "Извините, но эта функция доступна только преподавателям.")




                                                            # Реакция на нажатия кнопки
                                # функционал преподавателя
@bot.message_handler(regexp = "Заменить текущий csv лист")
def replace_csv(message: Message) -> None:
    if str(message.chat.id) == TEACHER_CHAT_ID:
        bot.send_message(message.chat.id, "Пожалуйста, отправьте новый CSV-файл.", reply_markup = ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, "Извините, но эта функция доступна только преподавателям.")

@bot.message_handler(regexp = "показать сниженные результаты учеников")
def replace_csv(message: Message) -> None:
    if str(message.chat.id) == TEACHER_CHAT_ID:
        bot.send_message(message.chat.id, "↴")
        #
        #
        #   Функционал для показа учеников со сниженныими показателями посещения и тд.
        #
    else:
        bot.send_message(message.chat.id, "Извините, но эта функция доступна только преподавателям.")






                                # функционал ученика
@bot.message_handler(regexp = "Показать мою статистику")    # получения имени пользователя 
def student_stats(message: Message) -> None:
    bot.send_message(message.chat.id, "Введите ваше имя, фамилию и номер группы раздельно.")
    bot.send_message(message.chat.id, "Для начала введите ваше имя: ", reply_markup = ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_name)

def get_name(message: Message) -> None:
    student_name = message.text
    bot.send_message(message.chat.id, "Теперь введите вашу фамилию: ")
    bot.register_next_step_handler(message, get_surname, student_name)

def get_surname(message: Message, student_name: str) -> None:       # получения фамилии пользователя 
    student_surname = message.text
    bot.send_message(message.chat.id, "Теперь введите номер вашей группы: ")
    bot.register_next_step_handler(message, get_group_number, student_name, student_surname)

def get_group_number(message: Message, student_name: str, student_surname: str) -> None:        # получения номера группы от пользователя
    student_group = message.text

    # Здесь должна быть логика поиска статистики студента
    # ...
    # ...
    # ...

    # После поиска статистики отправляем ее студенту
    
    markup = ReplyKeyboardMarkup() # возращение возможности пользоваться ReplyKeyboardMarkup для ученика 
    StudentStats = "Показать мою статистику"
    markup.add(StudentStats)

    bot.send_message(message.chat.id, f"Ваша статистика готова!: {student_name} {student_surname} {student_group}", reply_markup = markup)




bot.polling()
