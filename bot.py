import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters
)

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
TASKS, WALLET = range(2)
BOT_NAME = "SolAirdropHunterBot"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [[InlineKeyboardButton("✅ I Completed All Tasks", callback_data='tasks_done')]]
    
    await update.message.reply_text(
        f"👋 Hey {update.effective_user.first_name}! I'm {BOT_NAME} 🤖\n\n"
        "🔥 Get ready for the Mr. Kayblezzy Airdrop!\n\n"
        "📋 Complete these tasks:\n\n"
        "1. JOIN Telegram Channel ➜ t.me/Yakstaschannel\n"
        "2. JOIN Telegram Group ➜ t.me/yakstascapital\n"
        "3. FOLLOW Twitter ➜ twitter.com/bigbangdist10\n\n"
        "Click below when done:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True
    )
    return TASKS

async def tasks_done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🎉 Great job! We trust you didn't skip any tasks!\n\n"
        "💰 Now send your SOLANA wallet address:\n"
        "(Example: So1AmPLEaDDr3sss...)\n\n"
        "⚠️ Double-check for typos!"
    )
    return WALLET

async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    wallet = update.message.text.strip()
    
    # Simple validation
    if len(wallet) < 32 or len(wallet) > 44:
        await update.message.reply_text("❌ That doesn't look like a Solana address! Try again:")
        return WALLET
    
    await update.message.reply_text(
        f"🚀 CONGRATULATIONS {update.effective_user.first_name.upper()}!\n\n"
        "✅ You've qualified for Mr. Kayblezzy's exclusive airdrop!\n"
        "💸 100 SOL is being prepared for transfer to:\n"
        f"`{wallet}`\n\n"
        "⏳ Expect delivery within 24 hours!\n\n"
        "📢 Note: This is a TEST - no real SOL will be sent\n"
        "Thank you for participating!",
        parse_mode="Markdown"
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("❌ Airdrop registration cancelled")
    return ConversationHandler.END

def main() -> None:
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        logger.error("BOT_TOKEN environment variable missing!")
        return
    
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            TASKS: [CallbackQueryHandler(tasks_done, pattern="^tasks_done$")],
            WALLET: [MessageHandler(filters.TEXT & ~filters.COMMAND, wallet)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    
    # Start the Bot
    logger.info(f"{BOT_NAME} is starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
