from app.db.session import engine
from app.db.models import Base

# ایجاد جداول در اولین اجرا (برای سادگی تمپلیت)
Base.metadata.create_all(bind=engine)