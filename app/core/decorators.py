import functools
import traceback
import time
from collections import deque
from typing import Callable, Any
from app.core.logger import logger
from app.config import settings
from app.telegram.bot import notify_admin  # forward-declared usage (import-time safe via type: ignore)

# حافظهٔ ساده برای rate-limit پیام‌های خطا به ادمین
_error_times = deque(maxlen=50)

def should_notify_admin() -> bool:
    now = time.time()
    window = settings.ADMIN_ERROR_THROTTLE_SEC
    if not _error_times or (now - _error_times[-1]) >= window:
        _error_times.append(now)
        return True
    return False

# دکوریتر عمومی برای تمام هندلرها

def handler_guard(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:  # noqa
            tb = traceback.format_exc()
            logger.exception("Unhandled exception in handler %s", func.__name__)
            if should_notify_admin():
                try:
                    notify_admin(
                        f"\u26a0\ufe0f Exception in `{func.__name__}`:\n" + f"````\n{tb}\n````"
                    )
                except Exception:
                    logger.error("Failed to notify admin about error")
            # پیام کاربرپسند برای کاربر نهایی (اگر قابل دسترسی باشد)
            # در telebot خود هندلر مسئول پاسخ‌دهی است؛ اینجا سایلنت می‌مانیم
    return wrapper