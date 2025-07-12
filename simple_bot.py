from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# TU TOKEN AQUÍ
BOT_TOKEN = "7635211423:AAGKnLPi4lsPe0YjCA28P5Y2iL39dvw9Q2A"

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Bot funcionando ✅")

# Main
def main():
    print("Iniciando bot...")
    
    # Crear app
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Agregar comando
    app.add_handler(CommandHandler("start", start))
    
    # Iniciar
    print("Bot listo. Envía /start en Telegram")
    app.run_polling()

if __name__ == '__main__':
    main()