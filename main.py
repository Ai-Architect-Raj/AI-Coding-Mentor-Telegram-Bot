import os
from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from telegram.ext import (
ApplicationBuilder,
CommandHandler,
MessageHandler,
ContextTypes,
filters
)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
base_url="https://openrouter.ai/api/v1",
api_key=OPENROUTER_API_KEY
)

chat_history = {}

async def start(update: Update,
context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Hello. I teach coding, DSA, maths, AI/ML."
    )


async def chat(update: Update,
context: ContextTypes.DEFAULT_TYPE):

    user_id = str(update.message.from_user.id)
    user_text = update.message.text

    print("User:", user_text)

    if user_id not in chat_history:

        chat_history[user_id] = [
            {
            "role":"system",
            "content":"""

You are AI Mentor.

Teach:

Python
C++
Java
DSA
DBMS
OS
CN
SQL
Maths
Statistics
AI
Machine Learning
Deep Learning

Always:

Explain slowly
Give examples
Give code
Give practice questions

"""
            }
        ]

    chat_history[user_id].append(
        {
        "role":"user",
        "content":user_text
        }
    )

    try:

        response = client.chat.completions.create(

            model="mistralai/mistral-7b-instruct",

            messages=chat_history[user_id]

        )

        answer = response.choices[0].message.content

        chat_history[user_id].append(
            {
            "role":"assistant",
            "content":answer
            }
        )

        print("Bot:", answer)

        await update.message.reply_text(answer)

    except Exception as e:

        print(e)

        await update.message.reply_text(
            f"Error:\n{e}"
        )


app = ApplicationBuilder().token(
BOT_TOKEN
).build()

app.add_handler(
CommandHandler("start",start)
)

app.add_handler(
MessageHandler(
filters.TEXT & ~filters.COMMAND,
chat
)
)

print("BOT RUNNING")

app.run_polling()