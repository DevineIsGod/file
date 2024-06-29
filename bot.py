import os
import random
import string
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace with your Telegram Bot token
TOKEN = "7463848427:AAEc0gbiyaTJxI7hdsEOo_5r7jjRr6WC3RQ"

# Initialize the bot
bot = Bot(token=TOKEN)

# Function to generate a random string of alphabets
def generate_random_string(length=6):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

# Function to handle the /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to File Share Bot! Send me any file and I will provide you with a unique link to share.')

# Function to handle file uploads
def handle_file(update: Update, context: CallbackContext) -> None:
    file_id = update.message.document.file_id
    file = context.bot.get_file(file_id)
    
    # Generate a random string for the file link
    random_string = generate_random_string()
    
    file_extension = file.file_path.split('.')[-1]  # Get file extension
    file_name = f"{random_string}.{file_extension}"  # Construct unique file name
    file.download(os.path.join("files", file_name))  # Save file locally
    
    file_link = f"https://your-domain.com/files/{file_name}"  # Replace with your domain
    update.message.reply_text(f"File uploaded successfully! Here's your unique shareable link:\n{file_link}")

# Function to handle /batch command
def batch_command(update: Update, context: CallbackContext) -> None:
    # Generate a random string for the batch link
    random_string = generate_random_string(length=8)  # Adjust length as needed
    
    batch_link = f"https://your-domain.com/batch/{random_string}"  # Replace with your domain and endpoint
    update.message.reply_text(f"Here is your batch link:\n{batch_link}")

# Function to handle unknown commands
def unknown(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Sorry, I didn't understand that command.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document, handle_file))
    dispatcher.add_handler(CommandHandler("batch", batch_command))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    
