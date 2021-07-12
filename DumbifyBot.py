import logging
import os
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
import random

PORT = int(os.environ.get('PORT', 5000))

updater = Updater(token='1704982427:AAFL55HPUrj65dEG3mxraxbsNsqCGLINGp8', use_context=True)
dispatcher = updater.dispatcher

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


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path='1704982427:AAFL55HPUrj65dEG3mxraxbsNsqCGLINGp8')
updater.bot.setWebhook('https://desolate-citadel-02620.herokuapp.com/' + '1704982427:AAFL55HPUrj65dEG3mxraxbsNsqCGLINGp8')

def dumbifyMessage(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=dumbify(update.message.text))


dumbify_handler = MessageHandler(Filters.text & (~Filters.command), dumbifyMessage)
dispatcher.add_handler(dumbify_handler)


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


inline_dumbify_handler = InlineQueryHandler(inline_dumbify)
dispatcher.add_handler(inline_dumbify_handler)
