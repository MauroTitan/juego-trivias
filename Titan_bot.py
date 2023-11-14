import random
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = '6496171159:AAF5F6RMiodCOhCkre2OznSiVrKwipCJj18'
usuarios_unidos = []
trivias = [
    {'pregunta': '¿Cuál es la capital de Francia?', 'respuesta': 'París'},
    {'pregunta': '¿En qué año se descubrió América?', 'respuesta': '1492'},
    {'pregunta': '¿Cuál es el río más largo del mundo?', 'respuesta': 'Amazonas'},
    {'pregunta': '¿Quién pintó la Mona Lisa?', 'respuesta': 'Leonardo da Vinci'},
    {'pregunta': '¿Cuál es el planeta más grande del sistema solar?', 'respuesta': 'Júpiter'}
]

puntajes = {}

def start(update, context):
    chat_id = update.effective_chat.id
    user_id = update.message.from_user.id
    if user_id in usuarios_unidos:
       puntajes[chat_id] = 0
       context.bot.send_message(chat_id=chat_id, text='¡Bienvenido al juego de trivias! Responde correctamente a 5 preguntas para ganar puntos.')
       ask_question(update, context)
    else:
       context.bot.send_message(chat_id=update.effective_chat.id, text="Primero debes unirte al juego.")

def unirse(update, context):
    username = update.effective_user.username
    user_id = update.message.from_user.id
    if user_id not in usuarios_unidos:
        usuarios_unidos.append(user_id)
        puntajes[user_id] = 0
    if username in usuarios_unidos:
        context.bot.send_message(chat_id=update.effective_chat.id, text="¡Ya estás unido a la partida!")
    else:
        usuarios_unidos.append(username)
        update.message.reply_text("¡Te has unido a la partida!")
# Comando "/punto" para ver el puntaje actual
def punto(update, context):
    user_id = update.message.from_user.id
    puntos = puntajes.get(user_id, 0)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Tu puntaje actual es: {puntos}")

    # Función para manejar el comando /puntajes
def mostrar_puntajes(update, context):
    mensaje = "Puntajes totales:\n"
    for indice, (usuario, puntaje) in enumerate(sorted(puntajes.items(), key=lambda x: x[1], reverse=True), 1):
        nombre_usuario = context.bot.get_chat(usuario).username
        nombre_usuario_con_arroba = f"@{nombre_usuario}"
        mensaje += f"{indice}° {nombre_usuario_con_arroba}: {puntaje}\n"
    update.message.reply_text(mensaje)
    
def ask_question(update, context):
    chat_id = update.effective_chat.id
    user_id = update.message.from_user.id
    current_question = trivias[puntajes[user_id]]  # Reemplazar "puntajes[chat_id]" por "puntajes[user_id]"
    pregunta = current_question['pregunta']
    context.bot.send_message(chat_id=chat_id, text=pregunta)


def answer(update, context):
    chat_id = update.effective_chat.id
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username
    user_answer = update.message.text.lower()
    current_question = trivias[puntajes[user_id]]  # Reemplazar "puntajes[chat_id]" por "puntajes[user_id]"
    correct_answer = current_question['respuesta'].lower()


    if user_answer == correct_answer:
        puntajes[user_id] += 1
        puntaje_actual = puntajes[user_id]
        mensaje = '¡Respuesta correcta! Has ganado 1 punto.'
        update.message.reply_text(mensaje)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"@{user_name}, tu puntaje actual es {puntajes[user_id]}.")
    else:
        context.bot.send_message(chat_id=chat_id, text='Respuesta incorrecta. Sigue intentando.')

    if puntajes[user_id] == len(trivias):  # Reemplazar "puntajes[chat_id]" por "puntajes[user_id]"
        mostrar_ganador(update, context)
        del puntajes[user_id]
    else:
        ask_question(update, context)

def mostrar_ganador(update, context):
    max_puntaje = max(puntajes.values())
    ganadores = [usuario for usuario, puntaje in puntajes.items() if puntaje == max_puntaje]

    if len(ganadores) == 1:
        ganador = context.bot.get_chat(ganadores[0]).username
        mensaje = f"¡El ganador es @{ganador} con {max_puntaje} puntos!"
    else:
        ganadores_nombres = [context.bot.get_chat(usuario).username for usuario in ganadores]
        ganadores_string = ", ".join([f"@{nombre}" for nombre in ganadores_nombres])
        mensaje = f"Hay un empate entre {ganadores_string} con {max_puntaje} puntos cada uno."

    context.bot.send_message(chat_id=update.effective_chat.id, text=mensaje)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler("join", unirse))
    dp.add_handler(CommandHandler("punto", punto))
    dp.add_handler(CommandHandler("puntajes", mostrar_puntajes))
    dp.add_handler(CommandHandler("ganador", mostrar_ganador))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, answer))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()