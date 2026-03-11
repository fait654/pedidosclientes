import os
import re
from datetime import datetime
import telebot
from flask import Flask
from threading import Thread

# =========================
# CONFIGURACION
# =========================

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARPETA_REPORTES = os.path.join(BASE_DIR, "reportes")

if not os.path.exists(CARPETA_REPORTES):
    os.makedirs(CARPETA_REPORTES)

# =========================
# FLASK
# =========================

@app.route('/')
def home():
    return "Bot activo"


# =========================
# START
# =========================

@bot.message_handler(commands=['start'])
def start(message):

    mensaje = (
        "📄 BOT DE REPORTES\n\n"
        "Escribe una fecha para obtener el reporte.\n\n"
        "Formato:\n"
        "YYYY-MM-DD\n\n"
        "Ejemplo:\n"
        "2026-03-10"
    )

    bot.send_message(message.chat.id, mensaje)


# =========================
# MENSAJES
# =========================

@bot.message_handler(func=lambda message: True)
def recibir_mensaje(message):

    texto = message.text.strip()
    chat_id = message.chat.id

    print(f"[{datetime.now()}] Mensaje recibido: {texto}")

    patron_fecha = r"^\d{4}-\d{2}-\d{2}$"

    # validar formato
    if not re.match(patron_fecha, texto):

        bot.send_message(
            chat_id,
            "❌ Fecha incorrecta.\n\nUsa formato:\nYYYY-MM-DD\n\nEjemplo:\n2026-03-10"
        )
        return

    # validar fecha real
    try:
        datetime.strptime(texto, "%Y-%m-%d")

    except ValueError:

        bot.send_message(
            chat_id,
            "❌ Fecha inválida.\n\nEjemplo correcto:\n2026-03-10"
        )
        return

    nombre_pdf = f"resumen_pedidos_{texto}.pdf"
    ruta = os.path.join(CARPETA_REPORTES, nombre_pdf)

    if os.path.exists(ruta):

        try:

            with open(ruta, "rb") as archivo:

                bot.send_document(
                    chat_id,
                    archivo,
                    caption=f"📄 Reporte {texto}"
                )

        except Exception as e:

            bot.send_message(
                chat_id,
                f"❌ Error al enviar archivo:\n{e}"
            )

    else:

        bot.send_message(
            chat_id,
            f"⚠️ No encontré reporte para la fecha {texto}"
        )


# =========================
# EJECUTAR BOT
# =========================

def run_bot():
    bot.infinity_polling(timeout=60, long_polling_timeout=60)

Thread(target=run_bot).start()


# =========================
# EJECUTAR FLASK
# =========================

port = int(os.environ.get("PORT", 10000))

app.run(
    host="0.0.0.0",
    port=port
)