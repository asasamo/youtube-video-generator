import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from genVideo import generateVideo
from libs.share.toTiktok import toTiktok

logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s] [%(levelname)s] [%(funcName)s] - %(message)s")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Bot active!")
    logging.info(update.effective_chat.id)


async def genVideo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Invalid command!")
        return
    if os.getenv('CHAT_ID').split(' ').count(str(update.effective_chat.id)) == 0:
        return

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Generating video from r/{context.args[0]} with {int(context.args[1])} posts...")
    duration, seconds, filename = generateVideo(
        context.args[0], int(context.args[1]))

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Finished in {seconds} seconds!\nSending video ({duration}s, {round(float(os.path.getsize(filename) / 1024 / 1024), 2)} MBytes)...")

    logging.info("Uploading file")
    await context.bot.send_video(chat_id=update.effective_chat.id, video=open(filename, 'rb'),
                                 connect_timeout=10000, pool_timeout=10000, read_timeout=10000, write_timeout=10000)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Caption for instagram:")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Top {int(context.args[1])} posts from r/{context.args[0][0].upper() + context.args[0][1:]}!")
    logging.info("Done uploading!")


async def tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Invalid command!")
        return
    if os.getenv('CHAT_ID').split(' ').count(str(update.effective_chat.id)) == 0:
        return

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Generating video from r/{context.args[0]} with {int(context.args[1])} posts...")
    duration, seconds, filename = generateVideo(
        context.args[0], int(context.args[1]))

    await context.bot.send_message(chat_id=update.effective_chat.id, text=rf"Finished in {seconds} seconds!\Uploading video ({duration}s, {round(float(os.path.getsize(filename) / 1024 / 1024), 2)} MBytes) to Tiktok...")

    logging.info("Uploading file to Tiktok")
    toTiktok(filename)
    logging.info("Done uploading!")

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Caption for instagram:")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Top {int(context.args[1])} posts from r/{context.args[0][0].upper() + context.args[0][1:]}!")


if __name__ == '__main__':
    application = ApplicationBuilder().token(
        os.getenv('BOT_TOKEN')).build()

    start_handler = CommandHandler('start', start)
    genVideo_handler = CommandHandler('genVideo', genVideo)
    tiktok_handler = CommandHandler('tiktok', tiktok)

    application.add_handler(start_handler)
    application.add_handler(genVideo_handler)
    application.add_handler(tiktok_handler)

    application.run_polling()
