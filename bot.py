
from telegram.ext import Updater, CommandHandler, Job
import logging, datetime
import datetime_counter


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)
timers = dict()


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi! Use /set YYYY/MM/DD/HH/MM to set a timer, add your message after ":", if you need.')


def alarm(bot, job):
    """Function to send the alarm message"""
    bot.sendMessage(job.context, text=answer)


def set(bot, update, args, job_queue):
    """Adds a job to the queue"""

    user_text = update.message.text
    user_text = user_text.replace("/set ", "")
    if ':' in user_text:
        user_text_list = user_text.split(':')
        ndt = datetime.datetime.strptime(user_text_list[0], '%Y/%m/%d/%H/%M')
        dt_now = datetime.datetime.now()
        new_date = ndt - dt_now
        result = new_date.total_seconds()
        global answer
        answer = user_text_list[1]
    else:    
        ndt = datetime.datetime.strptime(user_text, '%Y/%m/%d/%H/%M')
        dt_now = datetime.datetime.now()
        new_date = ndt - dt_now
        result = new_date.total_seconds()
        global answer
        answer = 'Tutturu! Do your stuff!'
    
    chat_id = update.message.chat_id
    seconds = result

    try:
        due = int(result)
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return

        # Add job to queue
        job = Job(alarm, due, repeat=False, context=chat_id)
        timers[chat_id] = job
        job_queue.put(job)

        update.message.reply_text('Timer successfully set!')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set /set YYYY/MM/DD/HH/MM')


def unset(bot, update):
    """Removes the job if the user changed their mind"""
    chat_id = update.message.chat_id

    if chat_id not in timers:
        update.message.reply_text('You have no active timer')
        return

    job = timers[chat_id]
    job.schedule_removal()
    del timers[chat_id]

    update.message.reply_text('Timer successfully unset!')


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater("291987543:AAE91VCrIZ4IEqaFn27ZQzatGjBRKgxufm0")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler("set", set, pass_args=True, pass_job_queue=True))
    dp.add_handler(CommandHandler("unset", unset))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == "__main__":

    main()