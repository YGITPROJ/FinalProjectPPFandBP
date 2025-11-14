#
#
#
from assistant.models import AddressBook, NoteBook
from assistant.storage import load_data, save_data
from assistant import handlers
from assistant import styles
import shlex


def parse_input(user_input: str) -> tuple:
    """
    Парсить введений рядок на команду та аргументи
    Використовує shlex.split для коректної обробки лапок
    """
    try:
        parts = shlex.split(user_input)
    except ValueError as e:
        # Якщо користувач не закрив лапки
        print(f"{styles.ERROR}Помилка парсингу: {e} (можливо, незакриті лапки?)")
        return None, []

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
    print(f"{styles.INFO}Вітаю у персональному помічнику! (Введіть 'help' для довідки)")

    if "are_colors_enabled" in dir(styles):
        styles.are_colors_enabled()

    COMMANDS = {
        # --- Контакти ---
        "add-contact": handlers.add_contact,
        "update-contact": handlers.update_contact,
        "show-contact": handlers.show_contact,
        "show-all": handlers.show_all,
        "birthdays": handlers.birthdays,
        "find-contact": handlers.find_contact,
        # --- Нотатки ---
        "add-note": handlers.add_note,
        "add-tag": handlers.add_tag,
        "show-notes": handlers.show_notes,
        "find-note": handlers.find_note,
        "find-tag": handlers.find_tag,
        "sort-notes": handlers.sort_notes_by_tags,
        "delete-note": handlers.delete_note,
        # --- Загальні ---
        "help": handlers.show_help,
    }

    CONTACT_COMMANDS = [
        "add-contact",
        "update-contact",
        "show-contact",
        "show-all",
        "birthdays",
        "find-contact",
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

    GENERAL_COMMANDS = [
        "help",
    ]

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
                elif command in GENERAL_COMMANDS:
                    result = handler(args)
                else:
                    result = f"{styles.ERROR}Помилка диспетчера: команда '{command}' не приєднана до жодної категорії."

                print(result)

            else:
                print(f"{styles.ERROR}Невідома команда. Введіть 'help' для списку команд.")

        except KeyboardInterrupt:
            save_data(book, notes)
            print(f"\n{styles.WARNING}Вихід... Ваші дані збережено.")
            break
        except Exception as e:
            print(f"{styles.ERROR}Сталася критична помилка: {e}")


if __name__ == "__main__":
    main()