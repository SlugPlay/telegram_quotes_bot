# Modules------------------------------------------------------------------------------------------------------------------
import telegram 
import telegram.ext

import citaty_parser
import shiza_parser
import iron_parser
import db_func

import datetime 
import random
import pytz



# Addictions------------------------------------------------------------------------------------------------------------------
bot_information = open('bot_token.txt', 'r')
bot_logs = open('logs_bot.txt', 'w')
info_sub = open('info_subscribes.txt', 'r')
ready_info = [str(h) for h in info_sub.readlines()]
TOKEN = bot_information.readline()[:-1]



# Commands------------------------------------------------------------------------------------------------------------------
async def start_command(update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    await db_func.create_db()
    await db_func.create_profile(update.effective_user.id)
    
    # Buttons
    keyboard = [
        [
            telegram.KeyboardButton("Подписаться"),
            telegram.KeyboardButton("Не хочу"),
        ],
    ]
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder='Сделай правильный выбор')
    # Core Message
    await update.message.reply_text('Приветствую.\nХочешь получать немного мудрости на день?', reply_markup=reply_markup)
    

async def citaty_quote_command(update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    data = citaty_parser.find_quote()
    await update.message.reply_text(data)


async def shiza_quote_command(update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    data = shiza_parser.find_quote()
    await update.message.reply_text(data)


async def iron_quote_command(update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    data = iron_parser.find_quote()
    await update.message.reply_text(data)


async def random_quote_command(update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    all_quotes = [iron_parser.find_quote(), shiza_parser.find_quote(), citaty_parser.find_quote()]
    get_random = random.choice(all_quotes)
    await update.message.reply_text(get_random)


async def info_subscribes_command(update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(''.join(ready_info))



# Other functions------------------------------------------------------------------------------------------------------------------
# Getting information from InlineButtons
async def button_subscribe(update, _):
    global variant
    
    query = update.callback_query
    variant = query.data
    await query.answer()
    await query.edit_message_text(text=f"Выбор сделан")
    await db_func.edit_profile(update.effective_user.id, 'yes', variant)
    


# Error handler
async def error(update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
    print('Update "%s" caused error "%s"', update, context.error)

    
# Function for 08:00 mails
async def send_quotes(context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    subses = {'citaty': citaty_parser.find_quote(), 'shiza': shiza_parser.find_quote(), 'iron': iron_parser.find_quote()}
    data = db_func.get_users()
    for user in data:
        user_id = user[0]
        user_prefer = user[1]
        await context.bot.send_message(chat_id=user_id, text=subses.get(user_prefer))



# Message filter------------------------------------------------------------------------------------------------------------------
async def filter(update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if text == 'подписаться':
        prefers = [
            [telegram.InlineKeyboardButton('Большой сборник цитат из медиапространства', callback_data="citaty"),], 
            [telegram.InlineKeyboardButton('Записки больного шизофренией Максима Бамейро', callback_data="shiza"),], 
            [telegram.InlineKeyboardButton('Цитаты дядюшки Айро', callback_data="iron"),]
        ]
        reply_markup1 = telegram.InlineKeyboardMarkup(prefers)
        await update.message.reply_text('...', reply_markup=telegram.ReplyKeyboardRemove())
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=(update.effective_message.id+1))
        await update.message.reply_text('--- Выбери на какой источник цитат ты подпишешься ---\nЧтобы узнать подробнее про каждый источник набери:\n/info_subscribes', reply_markup=reply_markup1)
    elif text == 'не хочу':
        await db_func.edit_profile(update.effective_user.id, 'no', '-')
        await update.message.reply_text('Поешь говна, придурок', reply_markup=telegram.ReplyKeyboardRemove())

        




# Core------------------------------------------------------------------------------------------------------------------
def main():
    print('Starting bot...')
    app = telegram.ext.Application.builder().token(TOKEN).build()
    job_daily = app.job_queue

    app.add_handler(telegram.ext.CommandHandler('start', start_command))
    
    app.add_handler(telegram.ext.CallbackQueryHandler(button_subscribe))
    
    app.add_handler(telegram.ext.CommandHandler('citaty_quote', citaty_quote_command))
    app.add_handler(telegram.ext.CommandHandler('shiza_quote', shiza_quote_command))
    app.add_handler(telegram.ext.CommandHandler('iron_quote', iron_quote_command))
    app.add_handler(telegram.ext.CommandHandler('random_quote', random_quote_command))
    app.add_handler(telegram.ext.CommandHandler('info_subscribes', info_subscribes_command))

    app.add_handler(telegram.ext.MessageHandler(filters=None, callback=filter))

    app.add_error_handler(error)

    print('Polling...')
    job = job_daily.run_daily(send_quotes, time=datetime.time(19, 20, 00, 00, tzinfo=pytz.timezone('Europe/Moscow')), days=(0, 1, 2, 3, 4, 5, 6))
    app.run_polling(poll_interval=1)


if __name__ == '__main__':
    main()    
        



# Close addictions------------------------------------------------------------------------------------------------------------------
bot_information.close()
bot_logs.close()