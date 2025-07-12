import asyncio
from telegram import Bot

# PON TU TOKEN AQUÍ
TOKEN = "7635211423:AAGKnLPi4lsPe0YjCA28P5Y2iL39dvw9Q2A"

async def test():
    bot = Bot(token=TOKEN)
    
    # Obtener info del bot
    try:
        me = await bot.get_me()
        print(f"✅ Bot conectado: @{me.username}")
        print(f"Nombre: {me.first_name}")
        print(f"ID: {me.id}")
    except Exception as e:
        print(f"❌ Error: {e}")

# Ejecutar prueba
asyncio.run(test())