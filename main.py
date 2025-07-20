import os
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from converter import convert_file

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    file = await context.bot.get_file(document.file_id)

    input_path = f"input_{document.file_name}"
    await file.download_to_drive(input_path)

    if document.file_name.endswith(".pdf"):
        output_format = "epub"
    elif document.file_name.endswith(".epub"):
        output_format = "pdf"
    else:
        await update.message.reply_text("Only PDF or EPUB files are supported.")
        return

    await update.message.reply_text("Converting your file, please wait...")

    try:
        converted_path = convert_file(input_path, output_format)
        await update.message.reply_document(document=InputFile(converted_path))
    except Exception as e:
        await update.message.reply_text(f"Conversion failed: {e}")
    finally:
        os.remove(input_path)
        if os.path.exists(converted_path):
            os.remove(converted_path)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

if __name__ == '__main__':
    print("Bot is running...")
    app.run_polling()
