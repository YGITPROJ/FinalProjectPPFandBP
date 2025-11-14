#
#
#
import functools
from .models import AddressBook, Record, NoteBook, Note
from . import styles
from datetime import datetime

# Символи для "дерева"
T_BRANCH = "├──"
L_BRANCH = "└──"
V_LINE = "│  "
EMPTY = "   "


# --- NEW HELPER FUNCTION ---
def _parse_contact_args(args: list) -> dict:
    """
    Парсить список аргументів з ключами (-n, -p, -e, -b, -a) у словник
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

        # Чи є значення після ключа
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
                raise ValueError(
                    "Ключ '-b' (birthday) може бути вказано лише один раз."
                )
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
            return f"{styles.ERROR}ValueError: {e}"
        except KeyError as e:
            # Змінено, щоб коректно показувати ID або Ім'я
            return f"{styles.ERROR}KeyError: {e}"
        except AttributeError:
            return f"{styles.ERROR}AttributeError: Контакт не знайдено або невірний атрибут."
        except IndexError:
            return f"{styles.WARNING}Недостатньо аргументів."
        except Exception as e:
            return f"{styles.ERROR}Сталася непередбачена помилка: {e}"

    return inner


# Функція для пошуку контакту
def get_record(name: str, book: AddressBook) -> Record:
    """Знаходить запис або кидає KeyError"""
    record = book.find(name)
    if record is None:
        raise KeyError(f"Контакт '{name}' не знайдено.")
    return record


# Обробники для контактів
@input_error
def add_contact(args: list, book: AddressBook) -> str:
    """
    Створює новий контакт з опціональними полями
    Приймає: -n [name] (опціонально: -p [phone] -e [email] -b [bday] -a [address])
    -n є обов'язковим.
    Адресу вказувати в лапках: -a "123 Main St"
    """
    if not args:
        raise IndexError

    data = _parse_contact_args(args)

    if not data["name"]:
        raise ValueError("Ключ '-n' (ім'я) є обов'язковим.")

    if book.find(data["name"]):
        raise ValueError(f"Контакт '{data['name']}' вже існує.")

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
    Оновлює поля існуючого контакту (додає телефон, замінює email/bday/address)
    Приймає: -n [name] (опціонально: -p [phone] -e [email] -b [bday] -a [address])
    -n є обов'язковим для ідентифікації контакту
    -p, -e, -b, -a замінюють існуючі значення
    """
    if not args:
        raise IndexError

    data = _parse_contact_args(args)

    if not data["name"]:
        raise ValueError("Ключ '-n' (ім'я) є обов'язковим для ідентифікації контакту.")

    record = get_record(data["name"], book)

    if not any([data["phone"], data["email"], data["birthday"], data["address"]]):
        raise ValueError("Вкажіть хоча б одне поле для оновлення (-p, -e, -b, -a).")

    messages = []

    if data["phone"]:
        record.add_phone(data["phone"])
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
        return f"{styles.WARNING}Для контакту '{record.name.value}' не було надано даних для оновлення."


@input_error
def show_contact(args: list, book: AddressBook) -> str:
    """
    Показує один контакт у деревовидному форматі
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

    # "дерево" деталей
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
    Показує дні народження на 'N' днів вперед
    Приймає: [days] (за замовчуванням 7)
    Новий синтаксис: [days] [-d DD.MM.YYYY]
    -d: вказує початкову дату, з якої ведеться відлік
    """
    days = 7  # За замовчуванням
    reference_date = None

    args_list = list(args)

    if "-d" in args_list:
        try:
            idx = args_list.index("-d")

            if idx + 1 >= len(args_list):
                raise ValueError("Після прапора '-d' очікується дата.")

            date_str = args_list[idx + 1]

            try:
                reference_date = datetime.strptime(date_str, "%d.%m.%Y").date()
            except ValueError:
                raise ValueError(
                    f"Невірний формат дати '{date_str}'. Використовуйте DD.MM.YYYY"
                )

            args_list.pop(idx)  # Видаляє '-d'
            args_list.pop(idx)  # Видаляє 'date_str'

        except ValueError as e:
            raise e

    if len(args_list) > 1:
        raise ValueError(f"Неочікувані аргументи: {' '.join(args_list)}")

    if len(args_list) == 1:
        try:
            days = int(args_list[0])
            if days <= 0:
                raise ValueError("Кількість днів має бути додатнім числом.")
        except ValueError:
            raise ValueError(f"Невірний формат для кількості днів: '{args_list[0]}'")

    upcoming = book.get_upcoming_birthdays(days, reference_date=reference_date)

    if reference_date:
        start_day_str = f"з {reference_date.strftime('%d.%m.%Y')}"
    else:
        start_day_str = "від сьогодні"

    if not upcoming:
        return f"{styles.INFO}Немає найближчих днів народження протягом {days} днів ({start_day_str})."

    response = [
        f"{styles.SUCCESS}Дні народження протягом {days} днів ({start_day_str}):"
    ]
    for item in upcoming:
        response.append(
            f" {T_BRANCH} {styles.HIGHLIGHT}{item['name']} "
            f"{styles.INFO}({item['birthday_date']}) - Вітати: {item['congratulation_day']}"
        )

    if response:
        response[-1] = response[-1].replace(T_BRANCH, L_BRANCH)

    return "\n".join(response)


@input_error
def find_contact(args: list, book: AddressBook) -> str:
    """
    Пошук контактів за текстом
    Приймає: [query...]
    """
    query = " ".join(args)
    if not query:
        raise ValueError("Введіть пошуковий запит.")

    found = book.search(query)

    if not found:
        return (
            f"{styles.WARNING}Не знайдено контактів, що відповідають запиту '{query}'."
        )

    response = [f"{styles.SUCCESS}Контакти, що відповідають запиту '{query}':"]
    for record in found:
        response.append(str(record))
    return "\n".join(response)


# --- НОТАТКИ ---
@input_error
def add_note(args: list, notes: NoteBook) -> str:
    """
    Додає нотатку
    Приймає: [text...] (текст нотатки)
    """
    text = " ".join(args)
    if not text:
        raise ValueError("Текст нотатки не може бути порожнім.")

    note = Note(text)
    new_id = notes.add_note(note)
    return f"{styles.SUCCESS}Нотатку додано (ID: {new_id})"


@input_error
def add_tag(args: list, notes: NoteBook) -> str:
    """
    Додає теги до нотатки
    Приймає: [note_id] [tag1] [tag2] ...
    """
    if len(args) < 2:
        raise ValueError("Потрібно вказати ID нотатки та хоча б один тег.")

    note_id, *tags = args
    if not tags:
        raise ValueError("Введіть хоча б один тег.")

    note = notes.find_by_id(note_id)
    if note is None:
        raise KeyError(f"Нотатку з ID '{note_id}' не знайдено")

    for tag in tags:
        note.add_tag(tag)
    return f"{styles.SUCCESS}Теги {tags} додано до нотатки {note_id}."


@input_error
def show_notes(args: list, notes: NoteBook) -> str:
    """Показує всі нотатки"""
    if not notes.data:
        return f"{styles.WARNING}Книга нотаток порожня."

    response = [f"{styles.SUCCESS}--- Всі Нотатки ---"]
    # Сортуємо за ID (int) перед виводом
    for note_id in sorted(notes.data.keys()):
        response.append(str(notes.data[note_id]))
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
    if not args:
        raise IndexError
    note_id = args[0]
    notes.delete_note(note_id)  # Метод в NoteBook обробить помилку
    return f"{styles.SUCCESS}Нотатку {note_id} видалено."


@input_error
def update_note(args: list, notes: NoteBook) -> str:
    """
    Оновлює текст існуючої нотатки.
    Приймає: [note_id] [новий текст...]
    """
    if len(args) < 2:
        raise ValueError("Вкажіть ID нотатки та новий текст.")

    note_id = args[0]
    new_text = " ".join(args[1:])

    if not new_text:
        # Це дублює перевірку в `note.update_text`, але краще перевірити тут
        raise ValueError("Новий текст нотатки не може бути порожнім.")

    note = notes.find_by_id(note_id)
    if note is None:
        raise KeyError(f"Нотатку з ID '{note_id}' не знайдено.")

    note.update_text(new_text)
    return f"{styles.SUCCESS}Текст нотатки {note_id} оновлено."


@input_error
def sort_notes_by_tags(args: list, notes: NoteBook) -> str:
    """
    Сортує та виводить нотатки за тегами (за алфавітом першого тега)
    'args' не використовується
    """
    sorted_notes = notes.sort_by_tags()

    if not sorted_notes:
        return f"{styles.WARNING}Книга нотаток порожня, нічого сортувати."

    response = [f"{styles.SUCCESS}--- Нотатки, відсортовані за тегами ---"]
    for note in sorted_notes:
        response.append(str(note))
    return "\n".join(response)


# --- HELP ---


def show_help(args: list) -> str:
    """
    Виводить детальну довідку по всім командам
    'args' не використовується
    """
    H = styles.HIGHLIGHT  # Заголовок команди
    C = styles.INFO  # Коментар/Аргументи
    E = styles.SUCCESS  # Приклад
    G = styles.WARNING  # Загальний заголовок

    help_text = [
        f"{G}--- Загальні Команди ---",
        f"  {H}hello{C}: Вітання.",
        f"  {H}help{C}: Ця довідка.",
        f"  {H}exit{C} (або {H}close{C}): Зберегти дані та вийти.",
        "",
        f"{G}--- Робота з Контактами ---",
        f"  {H}add-contact {C}-n [Ім'я] [Опції...]",
        f"    {C}Створює новий контакт. {styles.ERROR}-n є обов'язковим.{C}",
        f"    {C}Опції: {H}-p [телефон] -e [email] -b [DD.MM.YYYY] -a [адреса]",
        f'    {E}Приклад: add-contact -n "John Doe" -p 1234567890 -e john@g.com',
        "",
        f"  {H}update-contact {C}-n [Ім'я] [Опції...]",
        f"    {C}Оновлює існуючий контакт (замінює поля). {styles.ERROR}-n є обов'язковим.{C}",
        f"    {C}Опції: {H}-p [телефон] -e [email] -b [DD.MM.YYYY] -a [адреса]",
        f'    {E}Приклад: update-contact -n "John Doe" -p 0987654321',
        "",
        f"  {H}show-contact {C}[Ім'я]",
        f"    {C}Показує детальну інформацію про один контакт.",
        f'    {E}Приклад: show-contact "John Doe"',
        "",
        f"  {H}show-all",
        f"    {C}Показує список всіх контактів.",
        "",
        f"  {H}find-contact {C}[Запит]",
        f"    {C}Шукає контакти за збігом в імені, телефоні, email тощо.",
        f"    {E}Приклад: find-contact John",
        "",
        f"  {H}birthdays {C}[N] [-d DD.MM.YYYY]",
        f"    {C}Показує дні народження протягом {H}N{C} днів (за замовч. 7).",
        f"    {C}Якщо вказано {H}-d{C}, відлік починається з вказаної дати.",
        f"    {E}Приклад 1: birthdays 10",
        f"    {E}Приклад 2: birthdays -d 01.01.2025",
        f"    {E}Приклад 3: birthdays 15 -d 01.01.2025",
        "",
        f"{G}--- Робота з Нотатками ---",
        f"  {H}add-note {C}[Текст нотатки...]",
        f"    {C}Додає нову нотатку.",
        f'    {E}Приклад: add-note "Це моя перша нотатка"',
        "",
        f"  {H}update-note {C}[ID] [Новий текст...]",
        f"    {C}Оновлює текст нотатки за її ID.",
        f"    {E}Приклад: update-note 12 \"Це оновлений текст.\"",
        "",
        f"  {H}show-notes",
        f"    {C}Показує список всіх нотаток (відсортованих за ID).",
        "",
        f"  {H}delete-note {C}[ID нотатки]",
        f"    {C}Видаляє нотатку за її числовим ID.",
        f"    {E}Приклад: delete-note 12",
        "",
        f"  {H}add-tag {C}[ID нотатки] [Тег1] [Тег2]...",
        f"    {C}Додає один або декілька тегів до нотатки.",
        f"    {E}Приклад: add-tag 12 work python",
        "",
        f"  {H}find-note {C}[Запит...]",
        f"    {C}Шукає нотатки, в тексті яких є збіг.",
        f"    {E}Приклад: find-note перша",
        "",
        f"  {H}find-tag {C}[Запит тега]",
        f"    {C}Шукає нотатки, що мають тег, який містить запит.",
        f"    {E}Приклад: find-tag work",
        "",
        f"  {H}sort-notes",
        f"    {C}Сортує нотатки за алфавітом (на основі першого тега).",
    ]
    return "\n".join(help_text)
