# Головний імпорт модулів
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
    Головна функція бота.
    """
    # Перевірка підключення додаткових пакетів
    # colorama
    styles.are_colors_enabled()

    # Завантажуємо дані при старті
    book, notes = load_data()
    print(f"{styles.INFO}Вітаю у персональному помічнику!")

    # Словник-диспетчер команд
    # Ключ - команда, значення - відповідна функція-обробник
    COMMANDS = {
        # --- Контакти ---
        "add-contact": handlers.add_contact,
        "add-phone": handlers.add_phone,
        "change-phone": handlers.change_phone,
        "add-birthday": handlers.add_birthday,
        "add-email": handlers.add_email,
        "add-address": handlers.add_address,
        "show-contact": handlers.show_contact,
        "show-all": handlers.show_all,
        "show-birthday": handlers.show_birthday,
        "birthdays": handlers.birthdays,
        # --- Нотатки ---
        "add-note": handlers.add_note,
        "add-tag": handlers.add_tag,
        "show-notes": handlers.show_notes,
        "find-note": handlers.find_note,
        "find-tag": handlers.find_tag,
        "sort-notes": handlers.sort_notes_by_tags,
        "delete-note": handlers.delete_note,
    }

    CONTACT_COMMANDS = [
        "add-contact",
        "add-phone",
        "change-phone",
        "add-birthday",
        "add-email",
        "add-address",
        "show-contact",
        "show-all",
        "show-birthday",
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
                else:
                    result = f"{styles.ERROR}Помилка диспетчера: невідомий тип команди."

                print(result)

            else:
                print(f"{styles.ERROR}Невідома команда. Спробуйте ще раз.")

        except KeyboardInterrupt:
            save_data(book, notes)
            print(f"\n{styles.WARNING}Вихід... Ваші дані збережено.")
            break
        except Exception as e:
            print(f"{styles.ERROR}Сталася критична помилка: {e}")


if __name__ == "__main__":
    main()
