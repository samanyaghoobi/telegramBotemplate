from telebot.custom_filters import AdvancedCustomFilter
from telebot.types import Message, CallbackQuery
from app.db.session import get_session
from app.db.models import User, Role
from app.config import settings

# فیلتر ادمین بر اساس دیتابیس، با امکان دسترسی به MAIN_ADMIN_ID از env

class IsAdminFilter(AdvancedCustomFilter):
    key = "is_admin"

    def check(self, message: Message | CallbackQuery, value):
        # value در decorator مثل is_admin=True استفاده می‌شود
        if isinstance(message, CallbackQuery):
            uid = message.from_user.id
        else:
            uid = message.from_user.id if getattr(message, "from_user", None) else message.chat.id

        if uid == settings.MAIN_ADMIN_ID:
            return True

        # چک در دیتابیس
        with get_session() as s:
            user = s.query(User).filter(User.telegram_id == uid).first()
            if not user:
                return False
            # نقش admin در جدول Roles
            admin_role = s.query(Role).filter(Role.name == "admin").first()
            if not admin_role:
                return False
            return admin_role in user.roles