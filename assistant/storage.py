#
#
#
import pickle
from .models import AddressBook, NoteBook
import os
from . import config


def save_data(book: AddressBook, notes: NoteBook, filename=config.DEFAULT_STORAGE_PATH):
    """
    Зберігає адресну книгу та нотатки в файл
    Шлях береться з config.py
    """
    # Створюємо папку (наприклад, "DB"), якщо її ще не існує
    # os.path.dirname("DB/assistant_data.pkl") -> "DB"
    # os.path.dirname("assistant_data.pkl") -> "" (порожній рядок)
    storage_dir = os.path.dirname(filename)
    # Створюємо папку, лише якщо вона вказана (не ".")
    if storage_dir and not os.path.exists(storage_dir):
        os.makedirs(storage_dir)
    # Зберігаємо обидва об'єкти у вигляді словника
    data_to_save = {"address_book": book, "note_book": notes}
    with open(filename, "wb") as f:
        pickle.dump(data_to_save, f)


def load_data(filename=config.DEFAULT_STORAGE_PATH) -> tuple:
    """
    Завантажує адресну книгу та нотатки з файлу.
    Шлях береться з config.py
    """
    try:
        with open(filename, "rb") as f:
            data_loaded = pickle.load(f)
            if isinstance(data_loaded, AddressBook):
                return data_loaded, NoteBook()
            book = data_loaded.get("address_book", AddressBook())
            notes = data_loaded.get("note_book", NoteBook())
            return book, notes
    except (FileNotFoundError, pickle.UnpicklingError, EOFError, TypeError):
        return AddressBook(), NoteBook()
