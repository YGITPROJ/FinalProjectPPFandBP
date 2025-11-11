# assistant/config.py
import os

# --- Налаштування Збереження Даних ---

# Папка для збереження даних.
# "DB" - створить папку DB у корені проекту.
# "." - зберігатиме прямо у корені проекту.
DATA_DIR = "DB"

# Ім'я файлу для збереження
DATA_FILENAME = "assistant_data.pkl"

# --- Сформований шлях ---
# Цей код автоматично з'єднує папку та ім'я файлу
# os.path.join("DB", "file.pkl") -> "DB/file.pkl"
# os.path.join(".", "file.pkl")  -> "file.pkl" (або просто "file.pkl")
DEFAULT_STORAGE_PATH = os.path.join(DATA_DIR, DATA_FILENAME)