import telebot
from bs4 import BeautifulSoup
from telebot import types
import requests
import time
import random
import re


TOKEN = '7437909784:AAHpQ7rrwqV0lZekLDyMkL9QAFM4ZbjBfNo'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Здравствуйте! Добро пожаловать в Налоговый Навигатор — вашего надежного помощника в мире налогов России. Если у вас есть вопросы или вам нужна помощь, я здесь, чтобы облегчить вам налоговое планирование и декларирование.")
    main_menu(message)

session = requests.Session()

# Задаем заголовки для сессии
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
})

def format_text(text):
    # Удаляем лишние пробелы и переносы строк
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Заменяем HTML знаки на соответствующие символы
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&amp;', '&', text)
    
    # Добавляем переносы строк между абзацами
    text = text.replace('. ', '.\n\n')
    
    
    return text

def get_text_with_links(url, message):
    # Добавляем задержку
    time.sleep(random.uniform(0.5, 2.0))
    
    # Отправляем запрос
    response = session.get(url)
    
    # Проверяем статус ответа
    if response.status_code == 200:
        
        soup = BeautifulSoup(response.text, 'html.parser')
        if message.text == "Транспортный налог":
        # Ищем элемент
            text_element = soup.find('div', class_='droppanel__frame _reserv-left text-container paragraph-base')
        elif message.text == "Земельный налог":
            text_element = soup.find('div', id='droppanel-get_card_Children_base_36581152')
        elif message.text =="Налог на недвижимое имущество физ. Лиц":
            text_element = soup.find('div', id='droppanel-get_card_Children_base_19353152')
        elif message.text =="Налоговые льготы":
            text_element = soup.find('div', id='droppanel-get_card_Children_base_16181152')
        elif message.text =="Частые вопросы":
            text_element = soup.find('section', class_='line-primary line-adaptive_540-leading')
        
        if text_element:
            # Извлекаем и форматируем текст
            raw_text = text_element.get_text(separator=' ', strip=False)
            formatted_text = format_text(raw_text)
            
            # Ищем все теги <a> внутри элемента
            links = text_element.find_all('a')
            
            # Форматируем ссылки
            for link in links:
                href = link.get('href')
                link_text = link.get_text()
                formatted_text = formatted_text.replace(link_text, f"[{link_text}]({href})")
            
            return formatted_text
        else:
            # Если элемент не найден, возвращаем сообщение об ошибке
            return "Ошибка: Не найден элемент с указанным классом."
    else:
        # Если статус ответа не 200, возвращаем сообщение об ошибке
        return f"Ошибка {response.status_code}: Не удалось получить данные с сайта."



def send_category_info(message):
    if message.text == "Транспортный налог":
        url = 'https://gu.spb.ru/knowledge-base/imushchestvennye-nalogi/'
        text = get_text_with_links(url, message)
        bot.send_message(message.chat.id, text)
        
    elif message.text == "Земельный налог":
        url = 'https://gu.spb.ru/knowledge-base/imushchestvennye-nalogi/'
        text = get_text_with_links(url, message)
        bot.send_message(message.chat.id, text)
    elif message.text == "Налог на недвижимое имущество физ. Лиц":
        url = 'https://gu.spb.ru/knowledge-base/imushchestvennye-nalogi/'
        text = get_text_with_links(url, message)
        bot.send_message(message.chat.id, text)
    elif message.text == "Налоговые льготы":
        url = 'https://gu.spb.ru/knowledge-base/imushchestvennye-nalogi/'
        text = get_text_with_links(url, message)
        bot.send_message(message.chat.id, text)
    elif message.text == "Частые вопросы":
        url = 'https://gu.spb.ru/knowledge-base/imushchestvennye-nalogi/'
        text = get_text_with_links(url, message)
        bot.send_message(message.chat.id, text)
        

def main_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    buttons = [
        types.KeyboardButton("Имущественные налоги – что это"),
        types.KeyboardButton("Единый налоговый счет – что это"),
        types.KeyboardButton("Налоговые режимы для малого и среднего бизнеса – что это"),
        types.KeyboardButton("Декларирование доходов физических лиц (3-НДФЛ) – что это"),
        types.KeyboardButton("Зарплата в конверте – что это")
    ]
    markup.add(*buttons)
    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=markup)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.endswith("что это"):
        # Отправить подменю соответствующей категории
        send_sub_menu(message, message.text)
    elif message.text == "Назад":
        # Вернуться в главное меню
        main_menu(message)
    else:
        # Отправка информации по категориям
        send_category_info(message)

# Функция отправки подменю
def send_sub_menu(message, category):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    back_button = types.KeyboardButton("Назад")
    if category == "Имущественные налоги – что это":
        bot.send_message(message.chat.id, "Если у вас в собственности есть машина, квартира, земельный участок или другая недвижимость, за неё нужно платить налог. В некоторых случаях предусмотрены налоговые льготы.", reply_markup=markup)
        buttons = [
            types.KeyboardButton("Транспортный налог"),
            types.KeyboardButton("Земельный налог"),
            types.KeyboardButton("Транспортный налог"),
            types.KeyboardButton("Налог на недвижимое имущество физ. Лиц"),
            types.KeyboardButton("Налоговые льготы"),
            types.KeyboardButton("Частые вопросы")
        ]
    elif category == "Единый налоговый счет – что это":
        bot.send_message(message.chat.id, "С 2023 года действует новый механизм уплаты налогов и страховых взносов. Теперь все платежи поступают на единый счёт.", reply_markup=markup)
        buttons = [
            types.KeyboardButton("Единый налоговый счет (ЕНС)"),
            types.KeyboardButton("Единый налоговый платеж (ЕНП)"),
            types.KeyboardButton("Сроки сдачи отчетов и уплаты налогов"),
            types.KeyboardButton("Сальдо ЕНС"),
            types.KeyboardButton("Частые вопросы")
        ]
    elif category == "Налоговые режимы для малого и среднего бизнеса – что это":
        bot.send_message(message.chat.id, "В России существует несколько специальных налоговых режимов, которыми могут пользоваться предприниматели. На этой странице рассказываем об особенностях упрощённой и патентной системах налогообложения, а также о налоге на профессиональный доход для самозанятых.", reply_markup=markup)
        buttons = [
            types.KeyboardButton("Упрощенная система налогообложения (УСН)"),
            types.KeyboardButton("Патентная сисетма налогообложения"),
            types.KeyboardButton("Налог на профессиональный доход"),
            types.KeyboardButton("Частые вопросы")
        ]
    elif category == "Декларирование доходов физических лиц (3-НДФЛ) – что это":
        bot.send_message(message.chat.id, "Как правило, налог на доходы физических лиц уплачивается автоматически — он удерживается с заработной платы. Однако в некоторых случаях гражданам нужно самостоятельно рассчитать сумму налога и подать декларацию.", reply_markup=markup)
        buttons = [
            types.KeyboardButton("Виды доходов, которые нужно декларировать"),
            types.KeyboardButton("Сроки подачи декларации"),
            types.KeyboardButton("Способы подачи декларации"),
            types.KeyboardButton("Сроки уплаты налога"),
            types.KeyboardButton("Размер налога"),
            types.KeyboardButton("Частые вопросы")
        ]
    elif category == "Зарплата в конверте – что это":
        bot.send_message(message.chat.id, "Рассказываем, чем рискуют работники, получающие заработную плату по «серым» схемам, и какую ответственность несут работодатели, скрывающие реальные доходы своих сотрудников.", reply_markup=markup)
        buttons = [
            types.KeyboardButton("Что такое «белая», «серая» и «черная» зарплата"),
            types.KeyboardButton("Риски для работников"),
            types.KeyboardButton("Последствия для работодателей"),
            types.KeyboardButton("Частые вопросы")
        ]
    
    markup.add(*buttons, back_button)
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)



bot.polling(none_stop=True)
