import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from functions import check_Bin, get_data
from flask import Flask, request
import time

load_dotenv()
TOKEN = os.getenv("TOKEN")
Commands = ["/checkbin","/gendata","/country"]
Countrys = ["de: Germany","it: Italia","gb: United Kingdom","us: United States"]

appflask = Flask(__name__)

@appflask.route('/your-webhook-path', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True))
    bot.process_new_updates([update])
    return 'OK'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Hello {update.effective_user.first_name} Here are the Commands => {Commands}")

async def cmds(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = '\n'.join(map(lambda item: item.replace("'", ""), Commands))
    await update.message.reply_text(f"Commands =>\n{result}\n")

async def checkbin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        arg = "".join(context.args)
        arg2 = int(arg)
        Message = check_Bin(arg2)
        await update.message.reply_text(f"Please Wait Checking the bin [ {arg2} ]")
        time.sleep(4)
        await update.message.reply_text(f"{Message}")
    else:
        await update.message.reply_text(f"please enter 6-8 digits!")

async def country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = '\n'.join(map(lambda item: item.replace("'", ""), Countrys))
    await update.message.reply_text(f"Here:\n{result}\nNOTE // PLEASE USE THE SHORTCUT FORMAT!!")

async def gendata(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        arg = "".join(context.args)
        await update.message.reply_text(f"Please wait this may take some time!")
        time.sleep(2)
        await update.message.reply_text(f"{get_data(arg)}")
    else:
        await update.message.reply_text(f"Please use the command /country and use a shortcut of the country in the 2nd argument!")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Something went wrong! error: {context.error}")

def run():
    global bot
    app = ApplicationBuilder().token(TOKEN).build()

    bot = app.bot

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cmds", cmds))
    app.add_handler(CommandHandler("checkbin", checkbin))
    app.add_handler(CommandHandler("country", country))
    app.add_handler(CommandHandler("gendata", gendata))
    app.add_error_handler(error_handler)

    app.run_polling()

if __name__ == "__main__":
    run()