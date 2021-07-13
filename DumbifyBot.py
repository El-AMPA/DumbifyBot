import logging
import os
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
import random

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger()
PORT = int(os.environ.get('PORT', 5000))

def dumbify(chain):
    chain = chain.lower()
    i = 0
    random.seed()
    min = 1
    max = 2
    amount = random.randint(min, max)
    while i < len(chain):
        substr = chain[i:i+amount]
        chain = chain[:i] + substr.upper() + chain[i+len(substr):]
        i += amount+1+random.randint(min, max)
        amount = random.randint(min, max)

    return chain


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="To use this bot, write @DumbifyBot followed by your message. For long messages just send me the text in private and I will dumbify it. Enjoy!")

def dumbifyMessage(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=dumbify(update.message.text))

def inline_dumbify(update, context):
    query = update.inline_query.query.lower()
    if not query:
        return

    query = dumbify(query)

    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query,
            title='Dumbify your message!',
            input_message_content=InputTextMessageContent(query)
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(
        token='1704982427:AAFL55HPUrj65dEG3mxraxbsNsqCGLINGp8', use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # handler adding
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), dumbifyMessage))
    dp.add_handler(InlineQueryHandler(inline_dumbify))

    # log all errors
    # dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path='1704982427:AAFL55HPUrj65dEG3mxraxbsNsqCGLINGp8')
    updater.bot.setWebhook('https://desolate-citadel-02620.herokuapp.com/' + '1704982427:AAFL55HPUrj65dEG3mxraxbsNsqCGLINGp8')

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    # updater.idle()


if __name__ == '__main__':
    main()
