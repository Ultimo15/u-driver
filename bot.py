from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CONFIGURACIÓN
BOT_TOKEN = "7635211423:AAGKnLPi4lsPe0YjCA28P5Y2iL39dvw9Q2A"
WEB_APP_URL = "https://shiny-train-x54pvp56q6qgh9q79-5000.app.github.dev"

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    welcome_text = f"""
🚖 *¡Bienvenido a U-Driver {user.first_name}!*

El servicio de mototaxi más rápido de San Antonio del Táchira.

¿Qué deseas hacer?
"""
    
    # Botones principales
    keyboard = [
        [InlineKeyboardButton("🚖 Pedir Viaje", web_app=WebAppInfo(url=f"{WEB_APP_URL}/cliente"))],
        [InlineKeyboardButton("🏍️ Soy Conductor", callback_data="conductor_menu")],
        [InlineKeyboardButton("❓ Ayuda", callback_data="help"),
         InlineKeyboardButton("📊 Mi Perfil", callback_data="profile")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

# Manejo de botones
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "conductor_menu":
        text = """
🏍️ *MENÚ CONDUCTOR*

Para trabajar con U-Driver necesitas una suscripción activa.

💰 Costo: $20,000 COP/semana
📱 Pago: Nequi o efectivo
"""
        keyboard = [
            [InlineKeyboardButton("📊 Mi Dashboard", web_app=WebAppInfo(url=f"{WEB_APP_URL}/conductor"))],
            [InlineKeyboardButton("💳 Activar Suscripción", callback_data="subscription")],
            [InlineKeyboardButton("🔙 Volver", callback_data="back_to_start")]
        ]
        
    elif query.data == "help":
        text = """
❓ *AYUDA U-DRIVER*

*Para Clientes:*
• Presiona "Pedir Viaje"
• Permite tu ubicación
• Elige tu destino
• Ofrece tu precio
• Espera confirmación

*Para Conductores:*
• Activa tu suscripción
• Accede al dashboard
• Acepta viajes disponibles
• Gana dinero

📞 Soporte: @UDriverSoporte
⚠️ Quejas: +573232350038
"""
        keyboard = [[InlineKeyboardButton("🔙 Volver", callback_data="back_to_start")]]
        
    elif query.data == "profile":
        text = f"""
👤 *TU PERFIL*

🆔 ID: `{query.from_user.id}`
📱 Usuario: @{query.from_user.username or 'Sin username'}
🏆 Viajes: 0
⭐ Calificación: 5.0

🎮 Nivel: Principiante
🏅 Puntos: 0
"""
        keyboard = [[InlineKeyboardButton("🔙 Volver", callback_data="back_to_start")]]
        
    elif query.data == "subscription":
        text = """
💳 *ACTIVAR SUSCRIPCIÓN*

Envía $20,000 COP a:
📱 Nequi: 3232350038

Luego envía captura de pantalla a:
📲 WhatsApp: +573232350038

Tu suscripción se activará en minutos.
"""
        keyboard = [[InlineKeyboardButton("🔙 Volver", callback_data="conductor_menu")]]
        
    elif query.data == "back_to_start":
        # Volver al menú principal
        user = query.from_user
        welcome_text = f"""
🚖 *¡Bienvenido a U-Driver {user.first_name}!*

El servicio de mototaxi más rápido de San Antonio del Táchira.

¿Qué deseas hacer?
"""
        keyboard = [
            [InlineKeyboardButton("🚖 Pedir Viaje", web_app=WebAppInfo(url=f"{WEB_APP_URL}/cliente"))],
            [InlineKeyboardButton("🏍️ Soy Conductor", callback_data="conductor_menu")],
            [InlineKeyboardButton("❓ Ayuda", callback_data="help"),
             InlineKeyboardButton("📊 Mi Perfil", callback_data="profile")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=welcome_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        return
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

# Main
def main():
    print("Iniciando U-Driver Bot...")
    
    # Crear app
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Agregar manejadores
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    # Iniciar
    print("Bot listo! Envía /start en Telegram")
    app.run_polling()

if __name__ == '__main__':
    main()