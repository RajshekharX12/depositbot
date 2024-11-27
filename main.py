import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from wallet import WalletManager
from send import SendUSDT
from receive import ReceiveUSDT
from utils import get_main_menu

# Initialize logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Modules
wallet_manager = WalletManager()
send_usdt = SendUSDT()
receive_usdt = ReceiveUSDT()

# /start command
def start(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    wallet_address = wallet_manager.create_wallet(user_id)

    update.message.reply_text(
        f"👋 Welcome to the USDT Bot!\n\n🪙 Your Wallet Address:\n`{wallet_address}`\n\n"
        "💵 Deposit funds to get started.",
        parse_mode="Markdown",
    )
    update.message.reply_text("Choose an option:", reply_markup=get_main_menu())

# Handle "Send"
def send(update: Update, context: CallbackContext):
    update.message.reply_text("💸 Please provide the recipient's wallet address:")
    context.user_data["action"] = "send"
    return "WAIT_FOR_ADDRESS"

def wait_for_address(update: Update, context: CallbackContext):
    recipient_address = update.message.text
    context.user_data["recipient_address"] = recipient_address
    update.message.reply_text("💵 How much USDT would you like to send?")
    return "WAIT_FOR_AMOUNT"

def wait_for_amount(update: Update, context: CallbackContext):
    try:
        amount = float(update.message.text)
        user_id = update.message.chat_id
        recipient_address = context.user_data["recipient_address"]

        sender_private_key = wallet_manager.get_wallet_private_key(user_id)
        sender_address = wallet_manager.get_wallet_address(user_id)

        result = send_usdt.send_funds(sender_private_key, sender_address, recipient_address, amount)
        update.message.reply_text(result, parse_mode="Markdown")
    except ValueError:
        update.message.reply_text("❌ Invalid amount. Please enter a valid number.")

# Handle "Receive"
def receive(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    wallet_address = wallet_manager.get_wallet_address(user_id)

    if wallet_address:
        update.message.reply_text(f"💰 Your Wallet Address:\n\n`{wallet_address}`", parse_mode="Markdown")
    else:
        update.message.reply_text("❌ Wallet not found. Please use /start to create one.")

# Main function
def main():
    updater = Updater(token=os.getenv("TELEGRAM_BOT_TOKEN"), use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.regex("💸 Send"), send))
    dispatcher.add_handler(MessageHandler(Filters.regex("💰 Receive"), receive))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, wait_for_address, pass_user_data=True))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, wait_for_amount, pass_user_data=True))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
