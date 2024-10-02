"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

POINT, OTHER = range(2)
reply_keyboard = [["Точка А", "Точка В", "Точка С"]]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Привет! Это бот для экскурсии по значимым местам горно-обогатительного комбината <Святогор> "
        "Отправь /cancel чтобы прекратить общение с ботом.\n\n"
        "О чём хочешь узнать?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            input_field_placeholder="Выбери одну из достопримечательностей"
        ),
    )

    return POINT


async def point(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    point = update.message.text
    logger.info("Point of %s: %s", update.message.from_user.username, point)
    if point == "Точка А":
        await update.message.reply_text(
            "Описание точки А, "
            "много полезных и интересных фактов.",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard,
                input_field_placeholder="Выбери одну из достопримечательностей"
            ),
        )
    elif point == "Точка В":
        await update.message.reply_photo(
            "krasnouralsk11.jpg",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard,
                input_field_placeholder="Выбери одну из достопримечательностей"
            ),
        )
    elif point == "Точка С":
        await update.message.reply_text(
            "Описание точки C, "
            "много полезных и интересных фактов.",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard,
                input_field_placeholder="Выбери одну из достопримечательностей"
            ),
        )
        await update.message.reply_photo(
            "caption.jpg",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard,
                input_field_placeholder="Выбери одну из достопримечательностей"
            ),
        )

    return


async def other(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text("Пока-пока!")

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(
        "7879267340:AAH99b-Bhwcalehykvkz-N8RfrxRq6x190M").build()

    # Add conversation handler with the states A, B, C
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            POINT: [MessageHandler(filters.Regex("^Точка (А|В|С)$"), point)],
            OTHER: [MessageHandler(~filters.Regex("^Точка (А|В|С)$"), other)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
