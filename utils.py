from telegram import ReplyKeyboardMarkup

def get_main_menu():
    """Returns the main menu keyboard."""
    return ReplyKeyboardMarkup(
        [["💸 Send", "💰 Receive"]],
        one_time_keyboard=True,
        resize_keyboard=True,
    )
