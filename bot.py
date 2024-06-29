import os
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace with your Telegram Bot token
TOKEN = "your_bot_token_here"

# Initialize the bot
bot = Bot(token=TOKEN)

# Function to handle the /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to File Share Bot! Send me any file and I will provide you with a link to share.')

# Function to handle file uploads
def handle_file(update: Update, context: CallbackContext) -> None:
    file_id = update.message.document.file_id
    file = context.bot.get_file(file_id)
    file.download(os.path.join("files", file.file_path.split("/")[-1]))  # Save file locally
    file_link = f"https://your-domain.com/files/{file.file_path.split('/')[-1]}"  # Replace with your domain
    update.message.reply_text(f"File uploaded successfully! Here's your shareable link:\n{file_link}")

# Function to handle unknown commands
def unknown(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Sorry, I didn't understand that command.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document, handle_file))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
