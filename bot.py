import logging
import json
import os
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
    ConversationHandler,
)

# Configuration
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
DATA_FILE = "bot_data.json"

# State constants for Conversation
SHIPPING_NAME, SHIPPING_COUNTRY, SHIPPING_ZIP, SHIPPING_ADDRESS = range(4)

# Load/Save Data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "admin_id": None,
        "crypto_addresses": {
            "BTC": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
            "ETH": "0x71C7656EC7ab88b098defB751B7401B5f6d8976F",
            "XMR": "44AFFq5kSi7Q6L3K2K5J3Z3A1S2B3C4D5E6F7G8H9I0J1K2L3M4N5O6P7Q8R9S0T"
        }
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

data = load_data()

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🌿 *Welcome to Dwarf Plug Official Bot!* 🌿\n\n"
        "I'm here to help you complete your order from our shop.\n\n"
        "✅ *Paste your order summary* from the website to begin.\n"
        "✅ *Ask questions* using the menu below.\n"
        "✅ *Secure & Discreet* processing."
    )
    keyboard = [
        [InlineKeyboardButton("📦 Shipping Info", callback_data="faq_shipping"),
         InlineKeyboardButton("💰 Payment Methods", callback_data="faq_payment")],
        [InlineKeyboardButton("🚀 Tracking", callback_data="faq_tracking"),
         InlineKeyboardButton("🍁 Quality", callback_data="faq_quality")],
        [InlineKeyboardButton("📦 Bulk Orders", callback_data="faq_bulk")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def faq_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    responses = {
        "faq_shipping": "📦 *Shipping Info*\n\nWe ship worldwide in odor-proof, vacuum-sealed, plain packaging. No mention of contents or our brand on the outside. Stealth is our priority.",
        "faq_payment": "💰 *Payment Methods*\n\nWe accept Bitcoin (BTC), Ethereum (ETH), Monero (XMR), and various Gift Cards (Amazon, Steam, etc.). Crypto is preferred for maximum privacy.",
        "faq_tracking": "🚀 *Tracking*\n\nTracking numbers are provided within 24-48 hours after payment confirmation. All packages are insured.",
        "faq_quality": "🍁 *Product Quality*\n\nWe source only AAA+ to AAAA+ premium flower. All concentrates and edibles are lab-tested for potency and purity.",
        "faq_bulk": "📦 *Bulk Orders*\n\nBulk discounts are applied automatically on the site. For orders over $2000, contact us directly for custom rates."
    }
    
    text = responses.get(query.data, "Information coming soon...")
    back_keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(back_keyboard), parse_mode="Markdown")

async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    welcome_text = (
        "🌿 *Welcome to Dwarf Plug Official Bot!* 🌿\n\n"
        "I'm here to help you complete your order from our shop.\n\n"
        "✅ *Paste your order summary* from the website to begin.\n"
        "✅ *Ask questions* using the menu below.\n"
        "✅ *Secure & Discreet* processing."
    )
    keyboard = [
        [InlineKeyboardButton("📦 Shipping Info", callback_data="faq_shipping"),
         InlineKeyboardButton("💰 Payment Methods", callback_data="faq_payment")],
        [InlineKeyboardButton("🚀 Tracking", callback_data="faq_tracking"),
         InlineKeyboardButton("🍁 Quality", callback_data="faq_quality")],
        [InlineKeyboardButton("📦 Bulk Orders", callback_data="faq_bulk")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

# Order Parsing
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if "Order Details" in text or "Total:" in text:
        context.user_data['order_summary'] = text
        await update.message.reply_text(
            "✅ *Order Received!*\n\nI need your shipping details to proceed. Please enter your *Full Name*:",
            parse_mode="Markdown"
        )
        return SHIPPING_NAME
    else:
        await update.message.reply_text("I didn't recognize that. Please paste your order summary from the website or use the menu.")
        return ConversationHandler.END

# Shipping Conversation
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['shipping_name'] = update.message.text
    await update.message.reply_text("Great. Now enter your *Country and City*:", parse_mode="Markdown")
    return SHIPPING_COUNTRY

async def get_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['shipping_country'] = update.message.text
    await update.message.reply_text("Enter your *Zip/Postal Code*:", parse_mode="Markdown")
    return SHIPPING_ZIP

async def get_zip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['shipping_zip'] = update.message.text
    await update.message.reply_text("Finally, enter your *Detailed Address* (Street, House/Apt #):", parse_mode="Markdown")
    return SHIPPING_ADDRESS

async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['shipping_address'] = update.message.text
    
    summary = (
        f"📋 *Order Confirmation*\n\n"
        f"{context.user_data['order_summary']}\n\n"
        f"📍 *Shipping To:*\n"
        f"{context.user_data['shipping_name']}\n"
        f"{context.user_data['shipping_country']}, {context.user_data['shipping_zip']}\n"
        f"{context.user_data['shipping_address']}\n\n"
        f"Please choose your payment method:"
    )
    
    keyboard = [
        [InlineKeyboardButton("BTC", callback_data="pay_BTC"),
         InlineKeyboardButton("ETH", callback_data="pay_ETH"),
         InlineKeyboardButton("XMR", callback_data="pay_XMR")],
        [InlineKeyboardButton("🎁 Gift Card", callback_data="pay_GIFT")]
    ]
    
    await update.message.reply_text(summary, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    
    if data['admin_id']:
        admin_msg = (
            f"🔔 *New Order Pending*\n\n"
            f"User: @{update.effective_user.username}\n"
            f"Summary: {context.user_data['order_summary']}"
        )
        await context.bot.send_message(chat_id=data['admin_id'], text=admin_msg, parse_mode="Markdown")
        
    return ConversationHandler.END

async def payment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    method = query.data.replace("pay_", "")
    
    if method == "GIFT":
        text = (
            "🎁 *Gift Card Payment*\n\n"
            "1. Purchase an Amazon or Steam gift card for the total amount.\n"
            "2. Scratch the code and take a CLEAR photo of the card + receipt.\n"
            "3. Send the photo here in this chat.\n\n"
            "We will verify and process your order immediately."
        )
    else:
        address = data['crypto_addresses'].get(method, "Address not set")
        text = (
            f"💰 *{method} Payment*\n\n"
            f"Please send the total amount to the following address:\n\n"
            f"`{address}`\n\n"
            f"⚠️ *Verify address before sending.*\n"
            f"Once sent, please send a screenshot of the transaction hash/confirmation."
        )
    
    await query.edit_message_text(text, parse_mode="Markdown")

# Admin Commands
async def set_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data['admin_id'] = update.effective_user.id
    save_data(data)
    await update.message.reply_text(f"Admin set to: {update.effective_user.username}")

async def set_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != data['admin_id']:
        return
    
    try:
        args = context.args
        coin = args[0].upper()
        addr = args[1]
        data['crypto_addresses'][coin] = addr
        save_data(data)
        await update.message.reply_text(f"✅ {coin} address updated.")
    except:
        await update.message.reply_text("Usage: /set_address <COIN> <ADDRESS>")

if __name__ == '__main__':
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN environment variable is not set.")

    application = ApplicationBuilder().token(TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)],
        states={
            SHIPPING_NAME: [MessageHandler(filters.TEXT & (~filters.COMMAND), get_name)],
            SHIPPING_COUNTRY: [MessageHandler(filters.TEXT & (~filters.COMMAND), get_country)],
            SHIPPING_ZIP: [MessageHandler(filters.TEXT & (~filters.COMMAND), get_zip)],
            SHIPPING_ADDRESS: [MessageHandler(filters.TEXT & (~filters.COMMAND), get_address)],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("start_admin", set_admin))
    application.add_handler(CommandHandler("set_address", set_address))
    application.add_handler(CallbackQueryHandler(faq_handler, pattern="^faq_"))
    application.add_handler(CallbackQueryHandler(main_menu_callback, pattern="^main_menu$"))
    application.add_handler(CallbackQueryHandler(payment_handler, pattern="^pay_"))
    application.add_handler(conv_handler)
    
    print("Bot is running...")
    application.run_polling()
