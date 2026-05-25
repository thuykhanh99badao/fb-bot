from telegram.ext import Application, MessageHandler, filters
import yt_dlp
import os

# Lấy token từ Render Environment Variables
TOKEN = os.getenv("7927052027:AAG5cd-mbUct9cIJG6GbIGlZLIh9nAEauWE")

async def download_fb(update, context):
    url = update.message.text.strip()

    # Kiểm tra link Facebook
    fb_domains = [
        "facebook.com",
        "fb.watch",
        "m.facebook.com",
        "stories"
    ]

    if not any(domain in url for domain in fb_domains):
        await update.message.reply_text(
            "📎 Gửi link Facebook/Reel/Story công khai"
        )
        return

    try:
        msg = await update.message.reply_text(
            "⏳ Đang tải..."
        )

        ydl_opts = {
            'outtmpl': 'video.%(ext)s',
            'format': 'best',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0'
            },
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                url,
                download=True
            )

            file = ydl.prepare_filename(info)

        with open(file, 'rb') as video:
            await update.message.reply_video(
                video=video
            )

        os.remove(file)

        await msg.delete()

    except Exception as e:
        await update.message.reply_text(
            f"❌ Lỗi: {str(e)}"
        )

app = Application.builder().token(TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT, download_fb)
)

print("Bot đang chạy...")

app.run_polling()