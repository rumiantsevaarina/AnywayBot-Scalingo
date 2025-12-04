import telebot
from telebot import types
from telebot.types import InputMediaPhoto # ⬅️ НОВЫЙ ИМПОРТ

# ==========================================
# ⚙️ ВАШИ НАСТРОЙКИ
# ==========================================

# 1. Вставьте ваш токен
TOKEN = '8559525719:AAEAxrNvWHvebaPkxzLLJzBKCKKaSpge_Kg'

# 2. Вставьте ваш ID
ADMIN_ID = 7769571045 

bot = telebot.TeleBot(TOKEN)

# ==========================================
# 📝 ТЕКСТЫ И ДАННЫЕ (Ваши новые тексты сохранены)
# ==========================================

TEXT_GREETING = (
    "⭐️ **Привет! Вместе со «Сколково» и акселератором ИТМО мы создали AnyWay:**\n\n"
    "Платформу, которая заменяет хаос поступления на четкий план действий\n"
    "Официальный запуск уже в **январе!**\n\n"
    "Оставь заявку сейчас и забери **скидку 50% на все функции!** 🎁"
)

TEXT_ABOUT = (
    "ℹ️ **Почему AnyWay решит все твои проблемы:**\n\n"
    "✅ Персональный навигатор - посторим маршрут до приказа о зачислении\n"
    "✅ Поможем выбрать профессию и вуз\n"
    "✅ Олимпиады вместо ЕГЭ: подберем олимпиады, которые реально выиграть\n"
    "✅ Страховка времени и денег: сможешь обеспечить гарантию поступления до ЕГЭ\n"
    "✅ Инсайты от первых лиц: свяжем со студентами любых вузов\n"
    "✅ Расскажем про все подводные камни в новых законах\n\n"
    "​Итог: Ты получаешь персональный план поступления с учетом всех нюансов"
)

# ==========================================
# 📊 ТАРИФЫ
# ==========================================
TARIFFS = [
    {
        'id': 'navi', 
        'name': 'Тариф «AI-Навигатор олимпиад»',
        'price': '499 ₽',
        'desc': 'Для тех, кто хочет получить 100% гарантию поступления в любой вуз за несколько месяцев',
        'images': [
            'https://i.ibb.co/JRmHR5Wc/8.png', 
            'https://i.ibb.co/b570HhCp/image.png'
        ]
    },
    {
        'id': 'control', 
        'name': 'Тариф «Полный контроль поступления»',
        'price': '990 ₽/модуль',
        'desc': 'Для родителей и учеников, которые не хотят упустить место в вузе из-за неправильной стратегии поступления',
        'images': [
            'https://i.ibb.co/1YVmn0mH/image.png',
            'https://i.ibb.co/NdNXHbbF/2.png'
        ]
    },
    {
        'id': 'vector', 
        'name': 'Тариф «Вектор профессии»',
        'price': '1990 ₽/модуль',
        'desc': 'Для тех, кто не определился с профессией и вузом и хочет обеспечить себе бюджет в институте за несколько месяцев',
        'images': [
            'https://i.ibb.co/mfk202q/7.png',
            'https://i.ibb.co/svfyVLbD/image.png'
        ]
    }
]

# Временное хранилище
user_data = {}

# ==========================================
# 🤖 ЛОГИКА БОТА
# ==========================================

def send_tariff_info(chat_id, tariff):
    """Отправляет изображения (2 шт.) и текст для одного выбранного тарифа."""
    # ИСПРАВЛЕНО: Правильное определение caption
    caption = (f"🎓 **{tariff['name']}**\n💰 Цена: {tariff['price']}\n\n{tariff['desc']}")
    
    # 1. Подготовка группы медиа
    media = []
    
    # Первое фото без подписи
    media.append(InputMediaPhoto(tariff['images'][0]))
    
    # Второе фото с подписью (Caption)
    if len(tariff['images']) > 1:
        media.append(InputMediaPhoto(tariff['images'][1], caption=caption, parse_mode='Markdown'))
    
    markup = types.InlineKeyboardMarkup()
    
    # ИЗМЕНЕНО: Кнопка передает ID тарифа
    btn = types.InlineKeyboardButton(f"🔥 Хочу {tariff['name']} (-50%)", callback_data=f"start_app_{tariff['id']}") 
    
    btn_back = types.InlineKeyboardButton("⬅️ Все тарифы", callback_data='show_tariffs')
    markup.add(btn)
    markup.add(btn_back)

    try:
        # 2. Отправка группы фото
        bot.send_media_group(chat_id, media)
        
        # 3. Отправка кнопки отдельно
        bot.send_message(chat_id, 
                         f"Нажмите, чтобы закрепить скидку на тариф *{tariff['name']}*:", 
                         reply_markup=markup, 
                         parse_mode='Markdown')
    except Exception as e:
        bot.send_message(chat_id, 
                         f"⚠️ *Ошибка загрузки изображений.* \n\n{caption}", 
                         reply_markup=markup, 
                         parse_mode='Markdown')
        print(f"MediaGroup Error: {e}")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn_about = types.InlineKeyboardButton("🧐 Узнать подробнее", callback_data='about')
    btn_tariffs = types.InlineKeyboardButton("📊 Посмотреть тарифы", callback_data='show_tariffs')
    
    # Кнопка с главной страницы запускает "Общую заявку"
    btn_discount = types.InlineKeyboardButton("🎁 Получить скидку 50%", callback_data='get_discount_generic')
    
    markup.add(btn_about)
    markup.add(btn_tariffs)
    markup.add(btn_discount)
    
    bot.send_message(message.chat.id, TEXT_GREETING, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    
    if call.data == "about":
        markup = types.InlineKeyboardMarkup()
        btn_tariffs = types.InlineKeyboardButton("📊 Тарифы", callback_data='show_tariffs')
        btn_discount = types.InlineKeyboardButton("🎁 Хочу скидку!", callback_data='get_discount_generic')
        markup.add(btn_tariffs, btn_discount)
        bot.edit_message_text(TEXT_ABOUT, chat_id, call.message.message_id, reply_markup=markup, parse_mode='Markdown')

    elif call.data == "show_tariffs":
        markup = types.InlineKeyboardMarkup()
        for tariff in TARIFFS:
            btn = types.InlineKeyboardButton(tariff['name'], callback_data=f"show_{tariff['id']}")
            markup.add(btn)
        try:
            bot.edit_message_text("👇 **Выберите тариф для просмотра:**", 
                                  chat_id, 
                                  call.message.message_id, 
                                  reply_markup=markup, 
                                  parse_mode='Markdown')
        except:
            bot.send_message(chat_id, "👇 **Выберите тариф для просмотра:**", reply_markup=markup, parse_mode='Markdown')


    elif call.data.startswith("show_"):
        tariff_id = call.data.split('_')[1]
        selected_tariff = next((t for t in TARIFFS if t['id'] == tariff_id), None)
        if selected_tariff:
            send_tariff_info(chat_id, selected_tariff)
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except Exception as e:
            pass
            
    # НОВАЯ ЛОГИКА: Заявка с главной страницы (Общая)
    elif call.data == "get_discount_generic":
        # Сохраняем информацию, что это общая заявка
        user_data[chat_id] = {'tariff': 'Общая (со страницы /start)'} 
        
        msg = bot.send_message(chat_id, "Отлично! Как к тебе обращаться? (Напиши имя)")
        bot.register_next_step_handler(msg, process_name_step)

    # НОВАЯ ЛОГИКА: Заявка с конкретного тарифа
    elif call.data.startswith("start_app_"):
        tariff_id = call.data.split('_')[2] 
        selected_tariff = next((t for t in TARIFFS if t['id'] == tariff_id), None)
        
        if selected_tariff:
            # СОХРАНЯЕМ ИМЯ ТАРИФА в user_data
            user_data[chat_id] = {'tariff': selected_tariff['name']}
        
        # Запускаем следующий шаг анкеты
        msg = bot.send_message(chat_id, "Отлично! Как к тебе обращаться? (Напиши имя)")
        bot.register_next_step_handler(msg, process_name_step)


# --- Шаги анкеты ---

def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        
        # Обновляем user_data, сохраняя имя и сохраняя старый tariff (если он есть)
        current_data = user_data.get(chat_id, {})
        current_data['name'] = name
        user_data[chat_id] = current_data
        
        msg = bot.send_message(chat_id, f"Приятно познакомиться, {name}! 👋\nТеперь напиши свой telegram ник (через @) или Email, чтобы ты точно получил самую большую скидку в январе!")
        bot.register_next_step_handler(msg, process_contact_step)
    except:
        bot.send_message(message.chat.id, "Ошибка. Нажми /start")

def process_contact_step(message):
    try:
        chat_id = message.chat.id
        contact = message.text
        
        user_info = user_data.get(chat_id, {})
        name = user_info.get('name', 'Неизвестно')
        username = message.from_user.username
        
        # НОВЫЙ КОД: Получаем название тарифа, иначе ставим "Не указан"
        tariff_name = user_info.get('tariff', 'Не указан/Неизвестно') 
        
        # 1. Отправка сообщения пользователю (Подтверждение)
        bot.send_message(chat_id, "✅ **Заявка принята!**\n\nЕсли ты видишь это сообщение, значит тебе важно твоё будущее.Ты будешь одним из первых, кто получит доступ по самой низкой цене.\n\nСпасибо, что ты с нами, вперед к победам! 🚀", parse_mode='Markdown')
        
        # 2. Отправка уведомления администратору
        lead_text = (
            f"🔥 **НОВАЯ ЗАЯВКА (AnyWay)!**\n\n"
            f"🎯 Тариф: **{tariff_name}**\n\n" # <--- СТРОКА С ТАРИФОМ
            f"👤 Имя: {name}\n"
            f"📞 Контакт: {contact}\n"
            f"🔗 Telegram: @{username if username else 'Скрыт'}"
        )
        bot.send_message(ADMIN_ID, lead_text)
        
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка. Попробуйте еще раз через /start")
        print(f"Error processing contact step: {e}")

if __name__ == '__main__':
    print("Бот AnyWay запущен...")
    bot.infinity_polling()