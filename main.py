import os
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("7875762200:AAHCCgarZqdDVrnv3HF6LlpD52t16t2wUvI")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a PDF or EPUB file, and I’ll convert it for you.")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()
    file_path = f"{update.message.document.file_name}"
    await file.download_to_drive(file_path)

    # Dummy conversion (just renaming for now)
    if file_path.endswith(".pdf"):
        output_path = file_path.replace(".pdf", ".epub")
        os.rename(file_path, output_path)
    elif file_path.endswith(".epub"):
        output_path = file_path.replace(".epub", ".pdf")
        os.rename(file_path, output_path)
    else:
        await update.message.reply_text("Only PDF or EPUB files are supported.")
        return

    await update.message.reply_document(document=InputFile(output_path))
    os.remove(output_path)

if __name__ == "__main__":
    app = ApplicationBuilder().token(7875762200:AAHCCgarZqdDVrnv3HF6LlpD52t16t2wUvI).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    app.run_polling()
