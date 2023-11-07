import logging
#from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Token del bot de Telegram
TOKEN = "6496171159:AAF5F6RMiodCOhCkre2OznSiVrKwipCJj18"

# Crear una instancia del updater y pasarle el token del bot
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Lista de jugadores y sus puntajes
puntajes = {}
usuarios_unidos = []
# Comando '/start'
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="¡Hola! Bienvenido al juego de cultura general.")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Comando '/unirte'
def unirte(update, context):
    user_id = update.message.from_user.id
    print("Usuario:", user_id)
    if user_id not in usuarios_unidos:
        usuarios_unidos.append(user_id)
        puntajes[user_id] = 0
        context.bot.send_message(chat_id=update.effective_chat.id, text="Te has unido al juego.")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Escribe /jugar para comenzar.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Ya te has unido al juego.")

unirte_handler = CommandHandler('unirte', unirte)
dispatcher.add_handler(unirte_handler)

# Comando '/jugar'
def jugar(update, context):
    pregunta = "¿Cuál es la capital de Francia?"
    context.bot.send_message(chat_id=update.effective_chat.id, text=pregunta)

jugar_handler = CommandHandler('jugar', jugar)
dispatcher.add_handler(jugar_handler)

# Comando '/puntuaciones'
def puntuaciones(update, context):
    tabla_puntajes = "Puntuaciones:\n\n"
    for jugador, puntaje in puntajes.items():
        tabla_puntajes += f"{jugador}: {puntaje}\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=tabla_puntajes)

puntuaciones_handler = CommandHandler('puntuaciones', puntuaciones)
dispatcher.add_handler(puntuaciones_handler)

# Comando '/ayuda'
def ayuda(update, context):
    lista_comandos = "Lista de comandos disponibles:\n\n" \
                     "/start - Iniciar el juego.\n" \
                     "/unirte - Unirse al juego.\n" \
                     "/jugar - Jugar una pregunta.\n" \
                     "/puntuaciones - Ver las puntuaciones.\n" \
                     "/ayuda - Mostrar esta lista de comandos."
    context.bot.send_message(chat_id=update.effective_chat.id, text=lista_comandos)

ayuda_handler = CommandHandler('ayuda', ayuda)
dispatcher.add_handler(ayuda_handler)

# Función para manejar las respuestas del usuario
def manejar_respuesta(update, context):
    respuesta = update.message.text
    usuario = update.effective_chat.username
    if respuesta == "París":
        puntajes[usuario] += 1
    puntaje_actual = puntajes[usuario]
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Tu puntaje actual es: {puntaje_actual}")

manejar_respuesta_handler = MessageHandler(Filters.text & (~Filters.command), manejar_respuesta)
dispatcher.add_handler(manejar_respuesta_handler)

# Iniciar el bot
updater.start_polling()