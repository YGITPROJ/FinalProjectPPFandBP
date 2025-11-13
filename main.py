#
# === Твій main.py (ПОВНА ВЕРСІЯ) ===
#
import difflib
from assistant.models import AddressBook, NoteBook
from assistant.storage import load_data, save_data
from assistant import handlers 
from assistant import styles 

def parse_input(user_input: str) -> tuple:
    """
    Парсить введений рядок на команду та аргументи
    """
    parts = user_input.split()
    if not parts:
        return None, []
    cmd = parts[0].strip().lower()
    args = parts[1:]
    return cmd, args


def main():
    """
    Головна функція бота
    """
    book, notes = load_data()
    print(f"{styles.INFO}Вітаю у персональному помічнику!")

    if "are_colors_enabled" in dir(styles):
        styles.are_colors_enabled()

    # Словник ВСІХ команд, які "щось роблять"
    COMMANDS = {
        # --- Контакти ---
        "add-contact": handlers.add_contact,
        "update-contact": handlers.update_contact,
        "show-contact": handlers.show_contact,
        "birthdays": handlers.birthdays,
        # (Додай сюди інші обробники контактів, якщо вони є)
        
        # --- Нотатки (всі, що ми додали) ---
        "add-note": handlers.add_note,           # Створити
        "find-note": handlers.find_note,       # Знайти за ID (фікс №1)
        "show-notes": handlers.show_notes,     # Показати всі
        "edit-note": handlers.edit_note_handler, # Редагувати (фікс №8)
        "delete-note": handlers.delete_note,   # Видалити (фікс №8)
        "search-notes": handlers.search_notes_handler, # Пошук за текстом (фікс №7)
        
        # --- Теги (Бонус) ---
        "add-tag": handlers.add_tag,
        "search-by-tag": handlers.search_by_tag,
        "sort-notes": handlers.sort_notes_by_tags,
    }

    # Списки для "диспетчера"
    CONTACT_COMMANDS = [
        "add-contact", "update-contact", "show-contact", "birthdays",
    ]

    NOTE_COMMANDS = [
        "add-note", "find-note", "show-notes", "edit-note", 
        "delete-note", "search-notes", "add-tag", 
        "search-by-tag", "sort-notes"
    ]
    
    # Список ВСІХ можливих слів для "вгадування"
    ALL_COMMANDS = list(COMMANDS.keys()) + ["hello", "close", "exit", "all"]

    while True:
        try:
            user_input = input(f"{styles.PROMPT}Введіть команду: ")
            command, args = parse_input(user_input)

            if command is None:
                continue # Пропускаємо порожній ввід

            if command in ["close", "exit"]:
                save_data(book, notes)
                print(f"{styles.WARNING}До побачення! Ваші дані збережено.")
                break

            elif command == "hello":
                print(f"{styles.INFO}Чим можу допомогти?")

            elif command == "all":
                # 'all' - особлива команда
                print(handlers.show_all(book, notes)) 

            elif command in COMMANDS:
                handler = COMMANDS[command] 
                result = ""
                
                if command in CONTACT_COMMANDS:
                    result = handler(args, book) # Передаємо 'book'
                elif command in NOTE_COMMANDS:
                    result = handler(args, notes) # Передаємо 'notes'
                else:
                    result = f"{styles.ERROR}Помилка диспетчера."

                print(result) # Друкуємо результат роботи

            else:
                # "Вгадування"
                matches = difflib.get_close_matches(
                    command, 
                    ALL_COMMANDS, 
                    n=1, 
                    cutoff=0.7
                )
                
                if matches:
                    print(f"{styles.ERROR}Невідома команда. Можливо, ви мали на увазі: '{matches[0]}'?")
                else:
                    print(f"{styles.ERROR}Невідома команда. Спробуйте ще раз.")

        except KeyboardInterrupt:
            save_data(book, notes)
            print(f"\n{styles.WARNING}Вихід... Ваші дані збережено.")
            break
        except Exception as e:
            # Обробка будь-яких інших помилок
            print(f"{styles.ERROR}Сталася критична помилка: {e}")


if __name__ == "__main__":
    main()
