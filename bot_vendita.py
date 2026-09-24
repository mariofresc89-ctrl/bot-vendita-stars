import logging
from telegram import Update, LabeledPrice
from telegram.ext import (
    Application,
    CommandHandler,
    PreCheckoutQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "8976156864:AAFL-F7Nj-BkuCNEujcLvciLl1mmimfZ7Ko"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

PREZZO_STARS = 50


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ciao! Questo bot vende un contenuto digitale.\n\n"
        "Clicca il pulsante qui sotto per acquistare con Telegram Stars."
    )
    await invia_invoice(update, context)


async def invia_invoice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_invoice(
        chat_id=update.effective_chat.id,
        title="Contenuto Digitale Premium",
        description="Accesso a un file/link esclusivo dopo il pagamento.",
        payload="contenuto_premium_v1",
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice(label="Contenuto Premium", amount=PREZZO_STARS)],
        start_parameter="acquisto_premium",
    )


async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)


async def pagamento_riuscito(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Grazie per l'acquisto!\n\n"
        "Ecco il tuo contenuto: https://esempio.com/contenuto-segreto\n\n"
        "(Sostituisci questo link con il tuo contenuto reale)"
    )
    payment = update.message.successful_payment
    logging.info(f"Pagamento ricevuto: {payment.total_amount} Stars da {update.effective_user.id}")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, pagamento_riuscito))

    print("Bot in esecuzione...")
    app.run_polling(allowed_updates=["message", "pre_checkout_query"])


if __name__ == "__main__":
    main()