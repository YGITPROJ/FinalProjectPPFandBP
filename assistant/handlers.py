import functools
from .models import AddressBook, Record, NoteBook, Note
from . import styles

# --- Символи для "дерева" ---
T_BRANCH = "├──"
L_BRANCH = "└──"
V_LINE = "│  "
EMPTY = "   "


def input_error(func):
    """
    Декоратор, який обробляє помилки вводу.
    Всі помилки валідації (ValueError),
    помилки пошуку (KeyError, AttributeError) та
    помилки вводу (IndexError) будуть оброблені
    та повернуть стилізоване повідомлення.
    """

    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"{styles.ERROR}ValueError: {e}"
        except KeyError as e:
            return f"{styles.ERROR}KeyError: Контакт {e} не знайдено."
        except AttributeError:
            return f"{styles.ERROR}AttributeError: Контакт не знайдено або невірний атрибут."
        except IndexError:
            return f"{styles.WARNING}Not enough arguments. Please provide full info."
        except Exception as e:
            return f"{styles.ERROR}An unexpected error occurred: {e}"

    return inner


def get_record(name: str, book: AddressBook) -> Record:
    """Знаходить запис або кидає KeyError."""
    record = book.find(name)
    if record is None:
        raise KeyError(name)
    return record


@input_error
def add_contact(args: list, book: AddressBook) -> str:
    """
    Створює новий контакт.
    Приймає: [name]
    """
    name = args[0]
    if book.find(name):
        raise ValueError(f"Contact '{name}' already exists.")

    record = Record(name)
    book.add_record(record)
    return f"{styles.SUCCESS}Контакт '{name}' успішно створено."


@input_error
def add_phone(args: list, book: AddressBook) -> str:
    """
    Додає телефону до існуючого контакту.
    Приймає: [name] [phone]
    """
    name, phone = args
    record = get_record(name, book)
    record.add_phone(phone)
    return f"{styles.SUCCESS}Телефон '{phone}' додано до контакту '{name}'."


@input_error
def change_phone(args: list, book: AddressBook) -> str:
    """
    Змінює телефон для існуючого контакту.
    Приймає: [name] [old_phone] [new_phone]
    """
    name, old_phone, new_phone = args
    record = get_record(name, book)
    record.edit_phone(old_phone, new_phone)
    return f"{styles.SUCCESS}Телефон для '{name}' змінено з '{old_phone}' на '{new_phone}'."


@input_error
def add_birthday(args: list, book: AddressBook) -> str:
    """
    Додає день народження до контакту.
    Приймає: [name] [dd.mm.yyyy]
    """
    name, bday_str = args
    record = get_record(name, book)
    record.add_birthday(bday_str)
    return f"{styles.SUCCESS}День народження додано для '{name}'."


@input_error
def add_email(args: list, book: AddressBook) -> str:
    """
    Додає email до контакту.
    Приймає: [name] [email]
    """
    name, email = args
    record = get_record(name, book)
    record.add_email(email)
    return f"{styles.SUCCESS}Email додано для '{name}'."


@input_error
def add_address(args: list, book: AddressBook) -> str:
    """
    Додає адресу до контакту.
    Приймає: [name] [address...] (адреса може бути з пробілами)
    """
    name, *address_parts = args
    address = " ".join(address_parts)
    if not address:
        raise ValueError("Address cannot be empty.")
    record = get_record(name, book)
    record.add_address(address)
    return f"{styles.SUCCESS}Адресу додано для '{name}'."


@input_error
def show_contact(args: list, book: AddressBook) -> str:
    """
    Показує один контакт в деревовидному форматі.
    Приймає: [name]
    """
    name = args[0]
    record = get_record(name, book)

    response = [f" {styles.HIGHLIGHT}{record.name.value}"]

    details = []
    if record.phones:
        details.append(("Phones", [p.value for p in record.phones]))
    if record.email:
        details.append(("Email", [record.email.value]))
    if record.address:
        details.append(("Address", [record.address.value]))
    if record.birthday:
        details.append(("Birthday", [str(record.birthday)]))

    if not details:
        response.append(f" {L_BRANCH} {styles.WARNING}No additional details.")
        return "\n".join(response)

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
    Показує всі контакти. 'args' не використовується,
    але присутній для сумісності з диспетчером
    """
    if not book.data:
        return f"{styles.WARNING}Адресна книга порожня."

    response = [f"{styles.SUCCESS}--- Всі Контакти ---"]
    for record in book.data.values():
        response.append(str(record))
    return "\n".join(response)


@input_error
def show_birthday(args: list, book: AddressBook) -> str:
    """
    Показує день народження контакту.
    Приймає: [name]
    """
    name = args[0]
    record = get_record(name, book)
    if record.birthday:
        return f"{styles.INFO}{record.name.value}'s birthday: {str(record.birthday)}"
    return f"{styles.WARNING}Birthday not set for {name}."


@input_error
def birthdays(args: list, book: AddressBook) -> str:
    """
    Показує дні народження на 'N' днів вперед.
    Приймає: [days] (за замовчуванням 7)
    """
    days = int(args[0]) if args else 7  # За замовчуванням 7 днів

    upcoming = book.get_upcoming_birthdays(days)

    if not upcoming:
        return f"{styles.INFO}Немає найближчих днів народження протягом {days} днів."

    response = [f"{styles.SUCCESS}Дні народження протягом наступних {days} днів:"]
    for item in upcoming:
        response.append(
            f" {T_BRANCH} {styles.HIGHLIGHT}{item['name']} "
            f"{styles.INFO}({item['birthday_date']}) - Вітати: {item['congratulation_day']}"
        )

    # Виправляємо останню гілку
    if response:
        response[-1] = response[-1].replace(T_BRANCH, L_BRANCH)

    return "\n".join(response)


@input_error
def add_note(args: list, notes: NoteBook) -> str:
    """
    Додає нотатку.
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
    Додає теги до нотатки.
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
    """Показує всі нотатки."""
    if not notes.data:
        return f"{styles.WARNING}Книга нотаток порожня."

    response = [f"{styles.SUCCESS}--- Всі Нотатки ---"]
    for note in notes.data.values():
        response.append(str(note))
    return "\n".join(response)


@input_error
def find_note(args: list, notes: NoteBook) -> str:
    """
    Пошук нотаток за текстом.
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
    Пошук нотаток за тегом.
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
    Видаляє нотатку за ID.
    Приймає: [note_id]
    """
    note_id = args[0]
    notes.delete_note(note_id)
    return f"{styles.SUCCESS}Нотатку {note_id} видалено."


@input_error
def sort_notes_by_tags(args: list, notes: NoteBook) -> str:
    """
    Сортує та виводить нотатки за тегами (за алфавітом першого тега).
    'args' не використовується.
    """
    sorted_notes = notes.sort_by_tags()

    if not sorted_notes:
        return f"{styles.WARNING}Книга нотаток порожня, нічого сортувати."

    response = [f"{styles.SUCCESS}--- Нотатки, відсортовані за тегами ---"]
    for note in sorted_notes:
        response.append(str(note))
    return "\n".join(response)
