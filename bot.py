import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

keyboard = [["✅ Сделано", "❌ Пропустил"], ["Уровень", "Параметры"]]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

user_stats = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_stats[user.id] = {"Сила": 0, "Разум": 0, "Дух": 0, "Уровень": 1}
    await update.message.reply_text(
        f"Привет, Медет! Сегодня ты снова в игре. Готов выполнять квесты?",
        reply_markup=reply_markup
    )

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_stats:
        user_stats[user_id]["Сила"] += 1
        await update.message.reply_text("Молодец! Сила увеличена.")

async def missed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Не сдавайся, Медет. Завтра вернёшься в строй!")

async def level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = user_stats.get(update.effective_user.id, {})
    level = stats.get("Уровень", 1)
    await update.message.reply_text(f"Твой текущий уровень: {level}")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = user_stats.get(update.effective_user.id, {})
    text = "\n".join(f"{k}: {v}" for k, v in stats.items())
    await update.message.reply_text(f"Твои параметры:\n{text}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("done", done))
    app.add_handler(CommandHandler("missed", missed))
    app.add_handler(CommandHandler("level", level))
    app.add_handler(CommandHandler("stats", stats))

    app.run_polling()

if __name__ == "__main__":
    main()
