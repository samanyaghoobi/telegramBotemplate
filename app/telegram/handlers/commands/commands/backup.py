import os
import subprocess
from datetime import datetime
from telebot.types import Message
from app.config import settings
from app.core.decorators import handler_guard

# فقط ادمین اصلی اجازهٔ بکاپ دارد (MAIN_ADMIN_ID)

def register(bot):
    @bot.message_handler(commands=["backup"])
    @handler_guard
    def backup_cmd(m: Message):
        if m.from_user.id != settings.MAIN_ADMIN_ID:
            bot.reply_to(m, "⛔️ شما دسترسی اجرای بکاپ را ندارید.")
            return

        ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        os.makedirs(settings.BACKUP_DIR, exist_ok=True)
        outfile = os.path.join(settings.BACKUP_DIR, f"pg-backup-{ts}.sql")

        env = os.environ.copy()
        env.update({
            "PGHOST": os.getenv("POSTGRES_HOST", settings.POSTGRES_HOST),
            "PGPORT": str(os.getenv("POSTGRES_PORT", settings.POSTGRES_PORT)),
            "PGUSER": os.getenv("POSTGRES_USER", settings.POSTGRES_USER),
            "PGPASSWORD": os.getenv("POSTGRES_PASSWORD", settings.POSTGRES_PASSWORD),
        })

        cmd = [
            "pg_dump",
            "-d", settings.POSTGRES_DB,
            "-F", "p",   # plain SQL
            "-f", outfile,
        ]

        try:
            subprocess.check_call(cmd, env=env)
            with open(outfile, "rb") as f:
                bot.send_document(settings.MAIN_ADMIN_ID, f, caption=f"📦 Backup: {os.path.basename(outfile)}")
        except subprocess.CalledProcessError:
            bot.reply_to(m, "❌ خطا در ایجاد بکاپ.")
        except Exception:
            bot.reply_to(m, "❌ خطای ناشناخته هنگام ارسال بکاپ.")