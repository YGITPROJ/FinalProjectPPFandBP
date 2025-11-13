#
#
#
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

    COMMANDS = {
        # --- Контакти ---
        "add-contact": handlers.add_contact,
        "update-contact": handlers.update_contact,
        "show-contact": handlers.show_contact,
        "show-all": handlers.show_all,
        "birthdays": handlers.birthdays,
        # --- Нотатки ---
        "add-note": handlers.add_note,
        "add-tag": handlers.add_tag,
        "show-notes": handlers.show_notes,
        "find-note": handlers.find_note,
        "find-tag": handlers.find_tag,
        "sort-notes": handlers.sort_notes_by_tags,
        "delete-note": handlers.delete_note,
        # --- Інше ---
        "help": handlers.show_help,  # <--- ДОДАНО: Додано 'help'
    }

    CONTACT_COMMANDS = [
        "add-contact",
        "update-contact",
        "show-contact",
        "show-all",
        "birthdays",
    ]

    NOTE_COMMANDS = [
        "add-note",
        "add-tag",
        "show-notes",
        "find-note",
        "find-tag",
        "sort-notes",
        "delete-note",
        
    ]
# <--- ДОДАНО: Новий список для команд, що не потребують 'book' або 'notes'
    OTHER_COMMANDS = ["help"]
    
    while True:
        try:
            user_input = input(f"{styles.PROMPT}Введіть команду: ")
            command, args = parse_input(user_input)

            if command is None:
                continue

            if command in ["close", "exit"]:
                save_data(book, notes)
                print(f"{styles.WARNING}До побачення! Ваші дані збережено.")
                break

            elif command == "hello":
                print(f"{styles.INFO}Чим можу допомогти?")

            elif command in COMMANDS:
                handler = COMMANDS[command]

                if command in CONTACT_COMMANDS:
                    result = handler(args, book)
                elif command in NOTE_COMMANDS:
                    result = handler(args, notes)
                # <--- ДОДАНО: Оновлений блок для обробки 'help'
                elif command in OTHER_COMMANDS:
                    result = handler()  # Виклик без 'args', 'book' чи 'notes'
                else:
                    result = f"{styles.ERROR}Помилка диспетчера: невідомий тип команди."

                print(result)

            else:
                # <--- ЗМІНЕНО: Покращене повідомлення про помилку
                print(
                    f"{styles.ERROR}Невідома команда. Введіть 'help' для списку команд."
                )

        except KeyboardInterrupt:
            save_data(book, notes)
            print(f"\n{styles.WARNING}Вихід... Ваші дані збережено.")
            break
        except Exception as e:
            print(f"{styles.ERROR}Сталася критична помилка: {e}")


if __name__ == "__main__":
    main()
