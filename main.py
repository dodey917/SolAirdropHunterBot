import telebot
from telebot import types

# Replace with your real bot token
BOT_TOKEN = 7811627288:AAEpzqhvv5GvEqRjSWhVx-oqwEHiOGcmFss

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        types.InlineKeyboardButton("✅ Join Channel", url="https://t.me/Yakstaschannel"),
        types.InlineKeyboardButton("✅ Join Group", url="https://t.me/yakstascapital"),
        types.InlineKeyboardButton("✅ Follow Twitter", url="https://twitter.com/bigbangdist10"),
        types.InlineKeyboardButton("🚀 Submit Wallet", callback_data="submit_wallet")
    )

    welcome_text = (
        "👋 Welcome to Mr. Kayblezzy2 Airdrop!\n\n"
        "To qualify for the test airdrop:\n"
        "1. Join our Channel\n"
        "2. Join our Group\n"
        "3. Follow our Twitter\n"
        "4. Submit your Solana wallet\n\n"
        "Click the buttons below to complete the tasks."
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "submit_wallet")
def ask_wallet(call):
    bot.answer_callback_query(call.id)
    msg = bot.send_message(call.message.chat.id, "📩 Please enter your Solana wallet address:")
    bot.register_next_step_handler(msg, handle_wallet_submission)

def handle_wallet_submission(message):
    wallet = message.text.strip()
    bot.send_message(
        message.chat.id,
        f"✅ Well done, hope you didn't cheat the system 😉\n\n"
        f"🎉 Congratulations! You passed Mr. Kayblezzy2 Airdrop Call.\n"
        f"💰 10 SOL is on its way to your wallet: `{wallet}`\n\n"
        f"(This is a test airdrop bot.)",
        parse_mode="Markdown"
    )

bot.infinity_polling()
