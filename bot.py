import telebot
from telebot import types
import requests  # For fetching memes from an API
import threading
from flask import Flask

# Replace with your real bot token
BOT_TOKEN = '7811627288:AAEpzqhvv5GvEqRjSWhVx-oqwEHiOGcmFss'

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask('')

# ------------------- New Meme Function -------------------
def get_random_meme():
    """Fetches a random meme from an API"""
    try:
        response = requests.get('https://meme-api.com/gimme', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data['url'], data['title']
    except Exception:
        pass
    return None, "Failed to fetch meme 😢"

# ------------------- Modified Start Command -------------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2  # Changed to 2 columns for better layout
    markup.add(
        types.InlineKeyboardButton("✅ Channel", url="https://t.me/Yakstaschannel"),
        types.InlineKeyboardButton("✅ Group", url="https://t.me/yakstascapital"),
        types.InlineKeyboardButton("✅ Twitter", url="https://twitter.com/bigbangdist10"),
        types.InlineKeyboardButton("😂 Get Meme", callback_data="get_meme"),  # NEW MEME BUTTON
        types.InlineKeyboardButton("🚀 Submit Wallet", callback_data="submit_wallet")
    )

    welcome_text = (
        "👋 Welcome to Mr. Kayblezzy2 Airdrop!\n\n"
        "To qualify for the test airdrop:\n"
        "1. Join our Channel\n"
        "2. Join our Group\n"
        "3. Follow our Twitter\n"
        "4. Submit your Solana wallet\n\n"
        "✨ **NEW**: Use /meme for funny content!"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

# ------------------- New Meme Command -------------------
@bot.message_handler(commands=['meme'])
def send_meme_command(message):
    """Handles /meme command"""
    meme_url, title = get_random_meme()
    if meme_url:
        bot.send_photo(message.chat.id, meme_url, caption=f"😂 {title}")
    else:
        bot.reply_to(message, "Couldn't fetch a meme right now. Try again later!")

# ------------------- Meme Button Handler -------------------
@bot.callback_query_handler(func=lambda call: call.data == "get_meme")
def send_meme_callback(call):
    """Handles meme button press"""
    bot.answer_callback_query(call.id)
    meme_url, title = get_random_meme()
    if meme_url:
        bot.send_photo(call.message.chat.id, meme_url, caption=f"😂 {title}")
    else:
        bot.send_message(call.message.chat.id, "Meme machine broke! Try again later.")

# ------------------- Existing Wallet Logic -------------------
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

# ------------------- Flask Keep-Alive -------------------
@app.route('/')
def home():
    return "Bot is running"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Start bot and Flask
if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    bot.infinity_polling()
