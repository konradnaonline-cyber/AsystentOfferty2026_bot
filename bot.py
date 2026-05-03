import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Bot Token (replace with your actual token)
TOKEN = "8788140321:AAGUoDbOmIHGdSRcNa2Sw9VQRFe90e4WWy4"

# Offers data structure
OFFERS = {
    "Konta Osobiste": [
        {"name": "UniCredit — Konto osobiste", "link": "https://tmlead.pl/redirect/863920_3112"},
        {"name": "Credit Agricole — Konto osobiste", "link": "https://tmlead.pl/redirect/863920_2395"},
        {"name": "Bank Pocztowy — Konto \"W Porządku\" z bonusem", "link": "https://tmlead.pl/redirect/863920_3070"},
    ],
    "Pożyczki": [
        {"name": "Miniratka — Pożyczka online na raty", "link": "https://tmlead.pl/redirect/863920_3128"},
    ],
    "Leasing": [
        {"name": "Leasing Online — Oferta leasingowa dobierana pod klienta", "link": "https://www.comperialead.pl/a/pp.php?link=cd10d8cad875eb71840ce9b42d9be07b&etykieta_=leasingonline"},
    ],
    "Fintechy z Bonusami": [
        {"name": "Trading 212 — Darmowa akcja do 100 EUR za depozyt od 1 EUR", "link": "https://www.trading212.com/invite/4DtDBJ2k7pg"},
    ],
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message with inline buttons to choose categories."""
    keyboard = [
        [InlineKeyboardButton(category, callback_data=category)]
        for category in OFFERS.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Cześć! Jestem AsystentOfferty2026. Pomagam znaleźć najlepsze oferty finansowe z bonusami. Wybierz kategorię:",
        reply_markup=reply_markup,
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()

    category = query.data
    if category in OFFERS:
        message_text = f"Oto oferty w kategorii {category}:\n\n"
        for offer in OFFERS[category]:
            message_text += f"{offer["name"]}\n"
            keyboard = [[InlineKeyboardButton("Sprawdź ofertę", url=offer["link"])]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(message_text, reply_markup=reply_markup)
            message_text = "" # Clear for next offer

        # Add "Wróć do menu" button
        keyboard = [[InlineKeyboardButton("Wróć do menu", callback_data="menu")] ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("", reply_markup=reply_markup)
    elif category == "menu":
        await start(update, context) # Go back to the main menu

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
