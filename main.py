import os
import logging
from scraper import get_feed, devtoTop, devtoLatest, get_cssTricks, get_echojs, get_sidebar, get_theVerge, get_tldr, get_medium, get_techcrunch, get_hackerNews, get_productHunt, get_wired, get_theNextWeb
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import responses
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from dotenv import load_dotenv

# Getiing bot token from env file
load_dotenv()
TOKEN = os.getenv('Bot_Token')
# The name of your app on Heroku
NAME = os.getenv('NAME')
# Port is given by Heroku
PORT = int(os.environ.get('PORT', '8443'))


'''
💡Use this version if you deploying it on repl.it
Add the bot token in secretes section
# Getiing bot token from env file
  Bot_Token = os.environ['Bot_Token']
'''


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Starting Bot...')


# We defined this fuction to use as commands
# all update.message are reply from bots to user
def start(update, context):
    update.message.reply_text(
        "Good day there 👋,\nAll accessible commands are listed here.\ndevto- Devto todays popular articles \ntheverge - The Verge articles \nsidebar - Sidebar articles \ntechcrunch - Tech Crunch articles \nhackernews - Hacker News articles \nwired - Wired articles \nthenextweb - The Next Web articles \ncsstricks - CSS Tricks articles \nproducthunt - Product Hunt articles \nechojs - EchoJS articles \nmedium - Medium articles \ntldr - TLDR tech news \nsocials - Social media  links \nsource_code - Source code link")


def cmd(update, context):
    update.message.reply_text(
        '/tldr - TLDR tech news\n/devto-Devto todays popular artical\n/medium - Medium articles\n/techcrunch - TechCrunch articles\n/hackerNews - HackerNews articles\n/theVerge - The Verge articles\n/quote - Random quote\n/socials - Social media links\n/source_code - Source code link')


# tldr new
def tldr(update, context):
    keyboard = [
        [
            InlineKeyboardButton("tech", callback_data='tech'),
            InlineKeyboardButton("science", callback_data='science'),
            InlineKeyboardButton("programming", callback_data='programming'),
            InlineKeyboardButton(
                "miscellaneous", callback_data='miscellaneous')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        '💡Choose a category from the list below.', reply_markup=reply_markup)

# devto News


def devTo(update: Update, context: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton(
                "Top Articles of the day", callback_data='topArticles'),
            InlineKeyboardButton(
                "Latest Articles", callback_data='latestArticles'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('What would you like to have?',
                              reply_markup=reply_markup)

# Medium Articles


def medium(update, context):
    keyboard = [
        [

            InlineKeyboardButton(
                "programming", callback_data='med_programming'),
            InlineKeyboardButton(
                "Data Science", callback_data='med_datascience')
        ],
        [
            InlineKeyboardButton("Technology", callback_data='med_Technology'),
            InlineKeyboardButton("Artificial-Intelligence",
                                 callback_data='med_AI')
        ],
        [
            InlineKeyboardButton("Python", callback_data='med_py'),
            InlineKeyboardButton("Humor", callback_data='med_humor')
        ]

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        'From the list below, pick a category.', reply_markup=reply_markup)


# Tech Crunch Articles


def techCrunch(update, context):
    data = get_feed('https://techcrunch.com/feed/')
    context.bot.send_message(
        chat_id=update.effective_chat.id, parse_mode="markdown", text=data)

# HackerNews


def hackerNews(update, context):
    data = get_feed('https://news.ycombinator.com/rss')
    context.bot.send_message(
        chat_id=update.effective_chat.id, parse_mode="markdown", text=data)


# Getting the The Verge Articles
def theVerge(update, context):
    data = get_feed('https://www.theverge.com/rss/index.xml')
    context.bot.send_message(
        chat_id=update.effective_chat.id, parse_mode="markdown", text=data)

# Getting the producthunt articles


def productHunt(update, context):
    data = get_feed('https://www.producthunt.com/feed')
    context.bot.send_message(
        chat_id=update.effective_chat.id, parse_mode="markdown", text=data)

# Getting all wired articles


def wired(update, context):
    data = get_feed('https://www.wired.com/feed/')
    context.bot.send_message(
        chat_id=update.effective_chat.id, parse_mode="markdown", text=data)


# Getting all sidebar
def sidebar(update, context):
    data = get_feed('https://sidebar.io/feed.xml')
    context.bot.send_message(
        chat_id=update.effective_chat.id, parse_mode="markdown", text=data)

# css tricks


def cssTricks(update, context):
    data = get_feed('https://css-tricks.com/feed/')
    context.bot.send_message(
        chat_id=update.effective_chat.id, parse_mode="markdown", text=data)

# the next web


def theNextWeb(update, context):
    data = get_feed('https://thenextweb.com/feed/')
    context.bot.send_message(
        chat_id=update.effective_chat.id, parse_mode="markdown", text=data)

# Echo Js


def echoJs(update, context):
    data = get_feed('https://echojs.com/rss')
    context.bot.send_message(
        chat_id=update.effective_chat.id, parse_mode="markdown", text=data)

# there two methods to crete functions to get repond from bot this is 2nd one


def socials(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="List of Socails are down below:\n {Github} https://github.com/amrohan\n\n {Twitter} https://twitter.com/rohansalunkhe_\n\n {Instagram} https://www.instagram.com/amrohann\n\n {Email} amrohanx@gmail.com")


def source_code(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="the source code can be accessed here\n Github\n https://github.com/amrohan/Dev-News-Bot")


def handle_message(update, context):
    text = str(update.message.text).lower()
    logging.info(f'User ({update.message.chat.id}) says: {text}')

    # Bot response
    response = responses.get_response(text)
    update.message.reply_text(response)


def error(update, context):
    # Logs errors
    logging.error(f'Update {update} caused error {context.error}')


# command Buttons
def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    query.answer()

    # Now we can use context.bot, context.args and query.message
    if query.data == 'topArticles':
        data = devtoTop()
        query.edit_message_text(parse_mode="html", text=data)
    elif query.data == 'latestArticles':
        data = devtoLatest()
        query.edit_message_text(parse_mode="html", text=data)
    elif query.data == 'tech':
        tech, science, programming, miscellaneous = get_tldr()
        query.edit_message_text(text=tech)
    elif query.data == 'science':
        tech, science, programming, miscellaneous = get_tldr()
        query.edit_message_text(text=science)
    elif query.data == 'programming':
        tech, science, programming, miscellaneous = get_tldr()
        query.edit_message_text(text=programming)
    elif query.data == 'miscellaneous':
        tech, science, programming, miscellaneous = get_tldr()
        query.edit_message_text(text=miscellaneous)
    elif query.data == 'med_Technology':
        data = get_medium('technology')
        query.edit_message_text(parse_mode="html", text=data)
    elif query.data == 'med_AI':
        data = get_medium('artificial-intelligence')
        query.edit_message_text(parse_mode="html", text=data)
    elif query.data == 'med_programming':
        data = get_medium('programming')
        query.edit_message_text(parse_mode="html", text=data)
    elif query.data == 'med_datascience':
        data = get_medium('data-science')
        query.edit_message_text(parse_mode="html", text=data)
    elif query.data == 'med_py':
        data = get_medium('python')
        query.edit_message_text(parse_mode="html", text=data)
    elif query.data == 'med_humor':
        data = get_medium('humor')
        query.edit_message_text(parse_mode="html", text=data)


# Run the programms from here
if __name__ == '__main__':

    APP_NAME = 'https://devnewsbot.herokuapp.com/'
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Commands handler which callback our commands when user ask for it
    dp.add_handler(CommandHandler('start', start))

    dp.add_handler(CommandHandler('help', help))

    dp.add_handler(CommandHandler('cmd', cmd))

    dp.add_handler(CommandHandler('socials', socials))

    dp.add_handler(CommandHandler('source_code', source_code))
    # tldr handler
    dp.add_handler(CommandHandler('tldr', tldr))
    # Dev To
    dp.add_handler(CommandHandler('devto', devTo))
    # Medium
    dp.add_handler(CommandHandler('medium', medium))
    # Tech Crunch Articles
    dp.add_handler(CommandHandler('techcrunch', techCrunch))
    # Hacker News
    dp.add_handler(CommandHandler('hackernews', hackerNews))
    # The Verge
    dp.add_handler(CommandHandler('theverge', theVerge))
    # Product Hunt
    dp.add_handler(CommandHandler('producthunt', productHunt))
    # Wired
    dp.add_handler(CommandHandler('wired', wired))
    # Sidebar
    dp.add_handler(CommandHandler('sidebar', sidebar))
    # CSS Tricks
    dp.add_handler(CommandHandler('csstricks', cssTricks))
    # The Next Web
    dp.add_handler(CommandHandler('thenextweb', theNextWeb))
    # Echo JS
    dp.add_handler(CommandHandler('echojs', echoJs))

    # Messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # CallbackQueryHandler
    dp.add_handler(CallbackQueryHandler(button))

    # Log all errors
    dp.add_error_handler(error)

    # Run the bot
    # Use polling command while local development or Use this command when you dont want to use webhooks
    updater.start_polling(1.0)

    # using webhook so that we can run the bot in heroku without having wasting of resources
    #updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, webhook_url=APP_NAME + TOKEN)
    # Idle state give bot time to go in idle
    updater.idle()
