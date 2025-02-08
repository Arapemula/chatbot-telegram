from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()

base_url = os.getenv("url")
bot = os.getenv("token_openai")
tele = os.getenv("token_tele")

api = OpenAI(api_key=bot, base_url=base_url)

# Handler untuk perintah /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo saya adalah atmin_bot beta v1, apakah ada yang bisa saya bantu?")


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    completion = api.chat.completions.create(
        #sesuaikan model yang kamu gunakan
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message},
        ],
        temperature=0.7,
        max_tokens=256,
    )

    ai_reply = completion.choices[0].message.content
    await update.message.reply_text(ai_reply)

def main():
    app = Application.builder().token(tele).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("Bot sedang berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
