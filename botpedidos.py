import os
import re
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

TOKEN = "8500053438:AAHsvHcOSDbqO24bi5mmHfSDXVeKP5Jvwfc"

# ruta absoluta a la carpeta reportes
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARPETA_REPORTES = os.path.join(BASE_DIR, "reportes")

# crear carpeta si no existe
if not os.path.exists(CARPETA_REPORTES):
    os.makedirs(CARPETA_REPORTES)

# mensaje inicial
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = (
        "📄 BOT DE REPORTES\n\n"
        "Escribe una fecha para obtener el reporte.\n\n"
        "Formato de fecha:\n"
        "YYYY-MM-DD\n\n"
        "Ejemplo:\n"
        "2026-03-10"
    )
    await update.message.reply_text(mensaje)

# función que procesa cualquier mensaje
async def recibir_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()
    print(f"[{datetime.now()}] Mensaje recibido: {texto}")

    patron_fecha = r"^\d{4}-\d{2}-\d{2}$"

    # validar formato
    if not re.match(patron_fecha, texto):
        await update.message.reply_text(
            "❌ Fecha incorrecta.\n\nUsa este formato:\nYYYY-MM-DD\n\nEjemplo:\n2026-03-10"
        )
        return

    # validar fecha real
    try:
        datetime.strptime(texto, "%Y-%m-%d")
    except ValueError:
        await update.message.reply_text(
            "❌ Fecha inválida.\n\nEjemplo correcto:\n2026-03-10"
        )
        return

    nombre_pdf = f"resumen_pedidos_{texto}.pdf"
    ruta = os.path.join(CARPETA_REPORTES, nombre_pdf)

    if os.path.exists(ruta):
        try:
            with open(ruta, "rb") as archivo:
                await update.message.reply_document(
                    document=archivo,
                    filename=nombre_pdf
                )
        except Exception as e:
            await update.message.reply_text(f"❌ Error al enviar el archivo: {e}")
    else:
        await update.message.reply_text(
            f"⚠️ No encontré reporte para la fecha {texto}"
        )

# crear bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_mensaje))

print("Bot funcionando con polling...")

# ejecutar polling (simple y confiable)
app.run_polling()