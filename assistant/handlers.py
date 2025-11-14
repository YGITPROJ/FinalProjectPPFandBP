#
#
#
import functools
from .models import AddressBook, Record, NoteBook, Note
from . import styles

# Символи для "дерева"
T_BRANCH = "├──"
L_BRANCH = "└──"
V_LINE = "│  "
EMPTY = "   "

# --- NEW HELPER FUNCTION ---
def _parse_contact_args(args: list) -> dict:
    """
    Парсить список аргументів з ключами (-n, -p, -e, -b, -a) у словник.
    """
    parsed_data = {
        "name": None,
        "phone": None,
        "email": None,
        "birthday": None,
        "address": None,
    }
    i = 0
    while i < len(args):
        key = args[i]

        # Перевірка, чи є значення після ключа
        if i + 1 >= len(args):
            raise ValueError(f"Відсутнє значення для ключа '{key}'")

        value = args[i + 1]

        if key == "-n":
            if parsed_data["name"]:
                raise ValueError("Ключ '-n' (ім'я) може бути вказано лише один раз.")
            parsed_data["name"] = value

        elif key == "-p":
            if parsed_data["phone"]:
                raise ValueError("Ключ '-p' (phone) може бути вказано лише один раз.")
            parsed_data["phone"] = value

        elif key == "-e":
            if parsed_data["email"]:
                raise ValueError("Ключ '-e' (email) може бути вказано лише один раз.")
            parsed_data["email"] = value

        elif key == "-b":
            if parsed_data["birthday"]:
                raise ValueError("Ключ '-b' (birthday) може бути вказано лише один раз.")
            parsed_data["birthday"] = value

        elif key == "-a":
            if parsed_data["address"]:
                raise ValueError("Ключ '-a' (address) може бути вказано лише один раз.")
            parsed_data["address"] = value

        else:
            raise ValueError(f"Невідомий ключ '{key}'. Дозволені: -n, -p, -e, -b, -a.")

        i += 2  # Перестрибуємо через ключ та його значення

    return parsed_data

# Декоратор для обробки помилок


def input_error(func):
    """
    Декоратор, який обробляє помилки вводу
    """

    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"{styles.ERROR}{e}"  # Виводимо тільки текст помилки
        except KeyError as e:
            return f"{styles.ERROR}Не знайдено: {e}"  # Більш загальне повідомлення
        except AttributeError:
            return f"{styles.ERROR}Контакт не знайдено або невірний атрибут."
        except IndexError:
            return (
                f"{styles.WARNING}Недостатньо аргументів. Введіть 'help' для довідки."
            )
        except Exception as e:
            return f"{styles.ERROR}Сталася непередбачена помилка: {e}"

    return inner


# --- ДОДАНО: Нова функція 'help' ---

# Словник для help, який легко редагувати
COMMANDS_HELP = {
    "Контакти": {
        "add-contact": "add-contact [name] phone [phone] email [email]...",
        "update-contact": "update-contact [name] phone [phone]...",
        "show-contact": "show-contact [name]",
        "show-all": "show-all",
        "birthdays": "birthdays (або -n [days])",
    },
    "Нотатки": {
        "add-note": "add-note [text...]",
        "add-tag": "add-tag [note_id] [tag...]",
        "show-notes": "show-notes",
        "find-note": "find-note [query...]",
        "find-tag": "find-tag [tag...]",
        "sort-notes": "sort-notes (сортує за тегами)",
        "delete-note": "delete-note [note_id]",
    },
    "Інші": {
        "hello": "hello (для привітання)",
        "help": "help (ця довідка)",
        "exit": "exit / close (вихід та збереження)",
    },
}


def show_help():
    """
    Формує та повертає рядок довідки у вигляді таблиці/дерева.
    """
    response = [f"\n{styles.SUCCESS}--- Довідка по Командам ---"]
    response.append(
        f"\n  {styles.HIGHLIGHT}{'Команда':<18} {styles.HIGHLIGHT}{'Приклад / Опис'}"
    )
    response.append(f"  {'-'*18} {'-'*50}")

    all_commands = []
    for category, commands in COMMANDS_HELP.items():
        response.append(f"\n {styles.INFO}{category}:")

        # Збираємо команди для коректного малювання гілок
        command_items = list(commands.items())
        for i, (cmd, desc) in enumerate(command_items):
            is_last = i == len(command_items) - 1
            branch = L_BRANCH if is_last else T_BRANCH

            line = f"  {branch} {styles.WARNING}{cmd:<18} {styles.PROMPT}- {desc}"
            response.append(line)

    response.append("\n")
    return "\n".join(response)


# Функція для пошуку контакту
def get_record(name: str, book: AddressBook) -> Record:
    """Знаходить запис або кидає KeyError."""
    record = book.find(name)
    if record is None:

        raise KeyError(f"Контакт '{name}'")
    return record


# Обробники для контактів
@input_error
def add_contact(args: list, book: AddressBook) -> str:
    """
    Створює новий контакт з опціональними полями.
    Приймає: -n [name] (опціонально: -p [phone] -e [email] -b [bday] -a [address])
    -n є обов'язковим.
    Адресу вказувати в лапках: -a "123 Main St"
    """
    if not args:
        raise IndexError

    name = args[0]
    if book.find(name):

        raise ValueError(f"Контакт '{name}' вже існує.")

    record = Record(data["name"])
    messages = []

    if data["phone"]:
        record.add_phone(data["phone"])
        messages.append(f"додано телефон {data['phone']}")

    if data["email"]:
        record.add_email(data["email"])
        messages.append(f"додано email {data['email']}")

    if data["birthday"]:
        record.add_birthday(data["birthday"])
        messages.append(f"додано день народження {data['birthday']}")

    if data["address"]:
        record.add_address(data["address"])
        messages.append(f"додано адресу {data['address']}")

    book.add_record(record)

    if messages:
        return f"{styles.SUCCESS}Контакт '{record.name.value}' створено ({', '.join(messages)})."
    else:
        return f"{styles.SUCCESS}Контакт '{record.name.value}' успішно створено."

@input_error
def update_contact(args: list, book: AddressBook) -> str:
    """
    Оновлює поля існуючого контакту (додає телефон, замінює email/bday/address).
    Приймає: -n [name] (опціонально: -p [phone] -e [email] -b [bday] -a [address])
    -n є обов'язковим для ідентифікації контакту.
    -p, -e, -b, -a замінюють існуючі значення.
    """
    if not args:
        raise IndexError

    data = _parse_contact_args(args)

    if not data["name"]:
        raise ValueError("Ключ '-n' (ім'я) є обов'язковим для ідентифікації контакту.")

    record = get_record(data["name"], book)

    # --- ЗМІНЕНО: "phones" на "phone" ---
    if not any([data["phone"], data["email"], data["birthday"], data["address"]]):
        raise ValueError("Вкажіть хоча б одне поле для оновлення (-p, -e, -b, -a).")

    messages = []

    # --- ЗМІНЕНО: Логіка для одного телефону ---
    if data["phone"]:
        record.add_phone(data["phone"])  # Просто викликаємо add_phone, який перезапише
        messages.append(f"оновлено телефон на {data['phone']}")

    if data["email"]:
        record.add_email(data["email"])
        messages.append(f"оновлено email на {data['email']}")

    if data["birthday"]:
        record.add_birthday(data["birthday"])
        messages.append(f"оновлено день народження на {data['birthday']}")

    if data["address"]:
        record.add_address(data["address"])
        messages.append(f"оновлено адресу на {data['address']}")

    if messages:
        return f"{styles.SUCCESS}Контакт '{record.name.value}' оновлено ({', '.join(messages)})."
    else:
        return (
            f"{styles.WARNING}Для контакту '{record.name.value}' не було надано даних для оновлення."
        )

@input_error
def show_contact(args: list, book: AddressBook) -> str:
    """
    Показує один контакт у деревовидному форматі.
    Приймає: [name]
    """
    name = args[0]
    record = get_record(name, book)

    response = [f" {styles.HIGHLIGHT}{record.name.value}"]

    details = []
    if record.phone:
        details.append(("Phone", [record.phone.value]))
    if record.email:
        details.append(("Email", [record.email.value]))
    if record.address:
        details.append(("Address", [record.address.value]))
    if record.birthday:
        details.append(("Birthday", [str(record.birthday)]))

    if not details:
        response.append(f" {L_BRANCH} {styles.WARNING}No additional details.")
        return "\n".join(response)

    # Малюємо "дерево" деталей
    for i, (title, items) in enumerate(details):
        is_last_detail = i == len(details) - 1
        branch = L_BRANCH if is_last_detail else T_BRANCH

        response.append(f" {branch} {styles.INFO}{title}:")

        item_prefix = f" {EMPTY if is_last_detail else V_LINE} "

        for j, item in enumerate(items):
            item_branch = L_BRANCH if j == len(items) - 1 else T_BRANCH
            response.append(f" {item_prefix}{item_branch} {item}")

    return "\n".join(response)


@input_error
def show_all(args: list, book: AddressBook) -> str:
    """
    Показує всі контакти. 'args' не використовується
    """
    if not book.data:
        return f"{styles.WARNING}Адресна книга порожня."

    response = [f"{styles.SUCCESS}--- Всі Контакти ---"]
    for record in book.data.values():
        response.append(str(record))
    return "\n".join(response)


@input_error
def birthdays(args: list, book: AddressBook) -> str:
    """
    Показує дні народження.
    Приймає: -n [days] (для вказання кількості днів)
    Якщо викликано без аргументів, запитує інтерактивно.
    """
    days_ahead = 7  # За замовчуванням

    try:
        if "-n" in args:
            days_index = args.index("-n") + 1
            days_ahead = int(args[days_index])
        elif not args:
            # Інтерактивний режим, якщо "birthdays" введено без аргументів
            days_str = input(
                f"{styles.PROMPT}Введіть кількість днів для прогнозу (Enter - 7, '0' - сьогодні): "
            )
            if days_str == "":
                days_ahead = 7
            else:
                days_ahead = int(days_str)
        else:
            # Для сумісності, якщо ввели "birthdays 10" (але '-n' - пріоритет)
            days_ahead = int(args[0])

    except (IndexError, ValueError):
        raise ValueError(
            f"Невірна кількість днів. Введіть число (напр., '7') або '-n 7'."
        )

    upcoming = book.get_upcoming_birthdays(days_ahead)

    if not upcoming:
        if days_ahead == 0:
            return f"{styles.INFO}Сьогодні ніхто не святкує день народження."
        return (
            f"{styles.INFO}Немає найближчих днів народження протягом {days_ahead} днів."
        )

    # Форматуємо у вигляді таблиці
    if days_ahead == 0:
        header = f"\n{styles.SUCCESS}--- Дні Народження Сьогодні ---"
    else:
        header = (
            f"\n{styles.SUCCESS}--- Дні Народження (наступні {days_ahead} днів) ---"
        )

    response = [header]
    # Заголовки таблиці
    response.append(
        f" {styles.HIGHLIGHT}{'Ім\'я':<25} {styles.HIGHLIGHT}{'Дата ДН':<12} {styles.HIGHLIGHT}Вітати"
    )
    response.append(styles.PROMPT + "-" * 60)  # Розділювач

    for item in upcoming:
        name_str = f" {styles.INFO}{item['name']:<25}"
        date_str = f" {styles.PROMPT}{item['birthday_date']:<12}"
        congrats_str = f" {styles.WARNING}{item['congratulation_day']}"
        response.append(name_str + date_str + congrats_str)

    return "\n".join(response)

@input_error
def find_contact(args: list, book: AddressBook) -> str:
    """
    Пошук контактів за текстом.
    Приймає: [query...]
    """
    query = " ".join(args)
    if not query:
        raise ValueError("Введіть пошуковий запит.")

    found = book.search(query)

    if not found:
        return f"{styles.WARNING}Не знайдено контактів, що відповідають запиту '{query}'."

    response = [f"{styles.SUCCESS}Контакти, що відповідають запиту '{query}':"]
    # Використовуємо той самий __str__ з Record, що і в show_all
    for record in found:
        response.append(str(record))
    return "\n".join(response)


# Нотатки
@input_error
def add_note(args: list, notes: NoteBook) -> str:
    """
    Додає нотатку
    Приймає: [text...] (текст нотатки)
    """
    text = " ".join(args)
    if not text:
        raise ValueError("Note text cannot be empty.")

    note = Note(text)
    notes.add_note(note)
    return f"{styles.SUCCESS}Нотатку додано (ID: {note.id})"


@input_error
def add_tag(args: list, notes: NoteBook) -> str:
    """
    Додає теги до нотатки
    Приймає: [note_id] [tag1] [tag2] ...
    """
    note_id, *tags = args
    if not tags:
        raise ValueError("Please provide at least one tag.")

    note = notes.find_by_id(note_id)
    if note is None:
        raise KeyError(f"Note with ID '{note_id}'")

    for tag in tags:
        note.add_tag(tag)
    return f"{styles.SUCCESS}Теги {tags} додано до нотатки {note_id}."


@input_error
def show_notes(args: list, notes: NoteBook) -> str:
    """Показує всі нотатки"""
    if not notes.data:
        return f"{styles.WARNING}Книга нотаток порожня."

    response = [f"{styles.SUCCESS}--- Всі Нотатки ---"]
    for note in notes.data.values():
        response.append(str(note))
    return "\n".join(response)


@input_error
def find_note(args: list, notes: NoteBook) -> str:
    """
    Пошук нотаток за текстом
    Приймає: [query...]
    """
    query = " ".join(args)
    found = notes.search_by_text(query)

    if not found:
        return f"{styles.WARNING}Не знайдено нотаток, що містять '{query}'."

    response = [f"{styles.SUCCESS}Нотатки, що відповідають запиту '{query}':"]
    for note in found:
        response.append(str(note))
    return "\n".join(response)


@input_error
def find_tag(args: list, notes: NoteBook) -> str:
    """
    Пошук нотаток за тегом
    Приймає: [tag_query]
    """
    tag_query = " ".join(args)
    found = notes.search_by_tag(tag_query)

    if not found:
        return f"{styles.WARNING}Не знайдено нотаток з тегом '{tag_query}'."

    response = [f"{styles.SUCCESS}Нотатки з тегом '{tag_query}':"]
    for note in found:
        response.append(str(note))
    return "\n".join(response)


@input_error
def delete_note(args: list, notes: NoteBook) -> str:
    """
    Видаляє нотатку за ID
    Приймає: [note_id]
    """
    note_id = args[0]

    notes.delete_note(note_id)
    return f"{styles.SUCCESS}Нотатку {note_id} видалено."


@input_error
def sort_notes_by_tags(args: list, notes: NoteBook) -> str:
    """
    Сортує та виводить нотатки за тегами (за алфавітом першого тега).
    'args' не використовується
    """
    sorted_notes = notes.sort_by_tags()

    if not sorted_notes:
        return f"{styles.WARNING}Книга нотаток порожня, нічого сортувати."

    response = [f"{styles.SUCCESS}--- Нотатки, відсортовані за тегами ---"]
    for note in sorted_notes:
        response.append(str(note))
    return "\n".join(response)
