from pathlib import Path
from app.core.logger import logger, LOG_DIR

def get_last_rotated_log() -> Path | None:
    # مثل bot.log.2025-08-08 یا bot.log.1 بسته به پلتفرم
    candidates = sorted(LOG_DIR.glob("bot.log*"))
    if not candidates:
        return None
    # آخرین فایل پیش از bot.log فعلی
    # ساده: اگر bot.log وجود دارد، قبلی‌ها انتهای لیست هستند
    for p in reversed(candidates):
        if p.name != "bot.log":
            return p
    return None