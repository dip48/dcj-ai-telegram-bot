import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from dotenv import load_dotenv

# Import your chatbot function
from Chatbot import ChatBot

# -------------------------------------------------
# LOAD ENV
# -------------------------------------------------
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in .env")

GroqAPIkey = os.getenv("GroqAPIkey")

if not GroqAPIkey:
    raise ValueError("GroqAPIkey not found in .env file")


# -------------------------------------------------
# LOGGING
# -------------------------------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# -------------------------------------------------
# COMMANDS
# -------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Dcj-ai-bot is online!\n\n"
        "Just send any message and I will reply.\n\n"
        "chat base bot only chat with this bot."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Start bot\n"
        "/help - Help info\n"
        "Send any text to chat with me"
    )

# -------------------------------------------------
# CHAT HANDLER
# -------------------------------------------------
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # Typing indicator
    await update.message.chat.send_action("typing")

    try:
        reply = ChatBot(user_text)
        await update.message.reply_text(reply)

    except Exception as e:
        logger.error(e)
        await update.message.reply_text(
            "⚠️ Something went wrong. Please try again."
        )

# -------------------------------------------------
# MAIN
# -------------------------------------------------
def main():
    print("Telegram Bot Started...")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    app.run_polling()

if __name__ == "__main__":
    main()
