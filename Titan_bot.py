from telegram.ext import *
import random
TOKEN = '6496171159:AAF5F6RMiodCOhCkre2OznSiVrKwipCJj18'
puntajes = {}  # Diccionario para almacenar los puntajes de los usuarios
usuarios_unidos = []  # Lista para almacenar los usuarios que se han unido al juego
trivias = [
    {'pregunta': '¿Cuál es la capital de Francia?', 'respuesta': 'París'},
    {'pregunta': '¿En qué año se descubrió América?', 'respuesta': '1492'},
    {'pregunta': '¿Cuál es el río más largo del mundo?', 'respuesta': 'Amazonas'},
    {'pregunta': '¿Quién pintó la Mona Lisa?', 'respuesta': 'Leonardo da Vinci'},
    {'pregunta': '¿Cuál es el planeta más grande del sistema solar?', 'respuesta': 'Júpiter'}
]
    
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="¡Hola! Bienvenido al juego de preguntas.")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Escribe /unirte para unirte al juego.")

def join(update, context):
    user_id = update.message.from_user.id
    if user_id not in usuarios_unidos:
        usuarios_unidos.append(user_id)
        puntajes[user_id] = 0
        context.bot.send_message(chat_id=update.effective_chat.id, text="Te has unido al juego.")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Escribe /jugar para comenzar.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Ya te has unido al juego.")

def play(update, context):
    chat_id = update.effective_chat.id
    puntajes[chat_id] = 0
    context.bot.send_message(chat_id=chat_id, text='¡Bienvenido al juego de trivias! Responde correctamente a 5 preguntas para ganar puntos.')
    ask_question(update, context)
    
def ask_question(update, context):
    chat_id = update.effective_chat.id
    current_question = trivias[puntajes[chat_id]]
    pregunta = current_question['pregunta']
    context.bot.send_message(chat_id=chat_id, text=pregunta)

def answer(update, context):
    chat_id = update.effective_chat.id
    user_answer = update.message.text.lower()
    current_question = trivias[puntajes[chat_id]]
    correct_answer = current_question['respuesta'].lower()
    if user_answer == correct_answer:
        puntajes[chat_id] += 1
        context.bot.send_message(chat_id=chat_id, text='¡Respuesta correcta! Has ganado 1 punto.')
    else:
        context.bot.send_message(chat_id=chat_id, text='Respuesta incorrecta. Sigue intentando.')

    if puntajes[chat_id] == len(trivias):
        context.bot.send_message(chat_id=chat_id, text='¡Has respondido todas las preguntas! Tu puntaje final es: {}.'.format(puntajes[chat_id]))
        del puntajes[chat_id]
    else:
        ask_question(update, context)

def leaderboard(update, context):
    if len(puntajes) > 0:
        sorted_puntajes = sorted(puntajes.items(), key=lambda x: x[1], reverse=True)
        leaderboard_text = "Puntuaciones:\n"
        for idx, (user_id, puntaje) in enumerate(sorted_puntajes):
            user_name = context.bot.get_chat_member(chat_id=update.effective_chat.id, user_id=user_id).user.username
            leaderboard_text += f"{idx+1}. {user_name}: {puntaje}\n"
        context.bot.send_message(chat_id=update.effective_chat.id, text=leaderboard_text)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No hay puntuaciones para mostrar.")

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Comandos disponibles:\n/unirte: Unirte al juego.\n/jugar: Empezar trivias.\n/puntuaciones: Ver las puntuaciones de los jugadores.\n/ayuda: Ver los comandos disponibles.")

def error(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ha ocurrido un error. Por favor, intenta nuevamente más tarde.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('unirte', join))
    dp.add_handler(CommandHandler('jugar', play))
    dp.add_handler(CommandHandler('puntuaciones', leaderboard))
    dp.add_handler(CommandHandler('ayuda', help))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()