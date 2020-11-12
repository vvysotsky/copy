from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from telegram import Bot, Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, Filters, MessageHandler, CommandHandler, Updater
from telegram.utils.request import Request
from ugc.models import Message, Profile

# декоратор для отлова ошибок
def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Произошла ошибка: {e}'
            print(error_message)
            raise e
    return inner

#функция do_echo, заменил get_or_create на get
@log_errors
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text
    try:
        p = Profile.objects.get( external_id=chat_id,)
    except ObjectDoesNotExist:
        update.message.reply_text(text='Ты не имеешь доступа сюда',)
        return       
    m = Message(profile=p, text=text,)
    m.save()
    reply_text = "Привет, сотрудник,\nТвой ID = {}\nID сообщения = {}\n{}".format(chat_id,m.pk, text)
    update.message.reply_text(text=reply_text,)


#функция do_count, заменил get_or_create на get
@log_errors
def do_count(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    try:
        p = Profile.objects.get( external_id=chat_id,)
    except ObjectDoesNotExist:
        update.message.reply_text(text='Ты не имеешь доступа сюда',)
        return
    count = Message.objects.filter(profile=p).count()
    update.message.reply_text(text=f'У вас {count} сообщений',)



class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        # 1 - правильно подключение
        request = Request(connect_timeout = 0.5, read_timeout = 1.0)
        bot = Bot(request=request, token=settings.TOKEN)
        print(bot.get_me())
        # 2 - обработчики
        updater = Updater(bot=bot,use_context=True,)
        
        command_handler1 = CommandHandler('count', do_count)
        updater.dispatcher.add_handler(command_handler1)

        message_handler = MessageHandler(Filters.text, do_echo)
        updater.dispatcher.add_handler(message_handler)
        # 3 - запустить бесконечную обработку входящих сообщений
        updater.start_polling()
        updater.idle()
