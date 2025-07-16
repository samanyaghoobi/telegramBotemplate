import os
import importlib.util
from os.path import join
from app.core.logger import logger

def load_handlers(bot, handlers_dir="app/telegram/handlers"):
    """
    همه فایل‌های .py را از پوشهٔ هندلرها لود می‌کند و تابع register(bot) هرکدام را صدا می‌زند.
    اطمینان حاصل می‌کند none_handler.py آخر لود شود.
    """
    handler_files = []

    for root, _, files in os.walk(handlers_dir):
        for filename in files:
            if filename.endswith(".py") and not filename.startswith("_"):
                file_path = join(root, filename)
                if filename == "none_handler.py":
                    continue
                handler_files.append(file_path)

    for file_path in handler_files:
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        try:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)  # type: ignore
            if hasattr(module, "register"):
                module.register(bot)
            logger.info(f"✅ Loaded handler: {file_path}")
        except Exception as e:
            logger.error(f"❌ Failed to load handler {file_path}: {e}")

    none_handler_path = join(handlers_dir, "none_handler.py")
    if os.path.isfile(none_handler_path):
        try:
            spec = importlib.util.spec_from_file_location("none_handler", none_handler_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)  # type: ignore
            if hasattr(module, "register"):
                module.register(bot)
            logger.info(f"✅ Loaded final handler: {none_handler_path}")
        except Exception as e:
            logger.error(f"❌ Failed to load final handler {none_handler_path}: {e}")