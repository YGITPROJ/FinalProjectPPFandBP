#
# === Твій handlers.py (ВИПРАВЛЕНО БЛОК НОТАТОК) ===
#
import functools
# ❗️ Імпортуємо ВСІ потрібні класи
from .models import AddressBook, Record, NoteBook, Note
from . import styles

# (Символи для дерева - T_BRANCH, L_BRANCH...)
T_BRANCH = "├──"
L_BRANCH = "└──"
V_LINE = "│  "
EMPTY = "   "

# (Твій декоратор @input_error)
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
            # ❗️ Я трохи змінив помилку, щоб вона обробляла і контакти, і нотатки
            return f"{styles.ERROR}KeyError: {e}" 
        except AttributeError as e:
            # ❗️ Я змінив це, щоб показувати СПРАВЖНЮ помилку
            return f"{styles.ERROR}AttributeError: {e}" 
        except IndexError:
            return f"{styles.WARNING}Недостатньо аргументів."
        except Exception as e:
            return f"{styles.ERROR}An unexpected error occurred: {e}"
    return inner


# Функція для пошуку контакту
def get_record(name: str, book: AddressBook) -> Record:
    """Знаходить запис або кидає KeyError."""
    record = book.find(name)
    if record is None:
        raise KeyError(f"Контакт {name} не знайдено.") # ❗️ Уточнив помилку
    return record


# -------------------------------------
# ОБРОБНИКИ ДЛЯ КОНТАКТІВ (Я НЕ ЧІПАВ ЦЕЙ КОД)
# -------------------------------------

@input_error
def add_contact(args: list, book: AddressBook) -> str:
    # (Твій код...)
    if not args:
        raise IndexError
    name = args[0]
    if book.find(name):
        raise ValueError(f"Contact '{name}' already exists.")
    record = Record(name)
    args_data = args[1:]
    messages = []
    i = 0
    while i < len(args_data):
        keyword = args_data[i].lower()
        try:
            if keyword == "phone":
                i += 1
                record.add_phone(args_data[i])
                messages.append(f"додано телефон {args_data[i]}")
            elif keyword == "email":
                i += 1
                record.add_email(args_data[i])
                messages.append(f"додано email {args_data[i]}")
            elif keyword == "birthday":
                i += 1
                record.add_birthday(args_data[i])
                messages.append(f"додано день народження {args_data[i]}")
            elif keyword == "address":
                i += 1
                address_parts = args_data[i:]
                if not address_parts:
                    raise IndexError
                address = " ".join(address_parts)
                record.add_address(address)
                messages.append("додано адресу")
                break
            else:
                raise ValueError(
                    f"Невідоме ключове слово '{args_data[i]}'. Очікувалось 'phone', 'email', 'birthday' або 'address'."
                )
        except IndexError:
            raise ValueError(f"Не вказано значення для '{keyword}'.")
        i += 1
    book.add_record(record)
    if messages:
        return f"{styles.SUCCESS}Контакт '{name}' створено ({', '.join(messages)})."
    else:
        return f"{styles.SUCCESS}Контакт '{name}' успішно створено."


@input_error
def update_contact(args: list, book: AddressBook) -> str:
    # (Твій код...)
    if not args:
        raise IndexError
    name = args[0]
    record = get_record(name, book)
    args_data = args[1:]
    if not args_data:
        raise ValueError("Вкажіть хоча б одне поле для оновлення (phone, email, etc.).")
    messages = []
    i = 0
    while i < len(args_data):
        keyword = args_data[i].lower()
        try:
            if keyword == "phone":
                i += 1
                record.add_phone(args_data[i])
                messages.append(f"додано телефон {args_data[i]}")
            elif keyword == "email":
                i += 1
                record.add_email(args_data[i])
                messages.append("оновлено email")
            elif keyword == "birthday":
                i += 1
                record.add_birthday(args_data[i])
                messages.append("оновлено день народження")
            elif keyword == "address":
                i += 1
                address_parts = args_data[i:]
                if not address_parts:
                    raise IndexError
                address = " ".join(address_parts)
                record.add_address(address)
                messages.append("оновлено адресу")
                break
            else:
                raise ValueError(
                    f"Невідоме ключове слово '{args_data[i]}'. Очікувалось 'phone', 'email', 'birthday' або 'address'."
                )
        except IndexError:
            raise ValueError(f"Не вказано значення для '{keyword}'.")
        i += 1
    if messages:
        return f"{styles.SUCCESS}Контакт '{name}' оновлено ({', '.join(messages)})."
    else:
        return (
            f"{styles.WARNING}Для контакту '{name}' не було надано даних для оновлення."
        )


@input_error
def show_contact(args: list, book: AddressBook) -> str:
    # (Твій код...)
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
def birthdays(args: list, book: AddressBook) -> str:
    # (Твій код...)
    days = int(args[0]) if args else 7
    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return f"{styles.INFO}Немає найближчих днів народження протягом {days} днів."
    response = [f"{styles.SUCCESS}Дні народження протягом наступних {days} днів:"]
    for item in upcoming:
        response.append(
            f" {T_BRANCH} {styles.HIGHLIGHT}{item['name']} "
            f"{styles.INFO}({item['birthday_date']}) - Вітати: {item['congratulation_day']}"
        )
    if response:
        response[-1] = response[-1].replace(T_BRANCH, L_BRANCH)
    return "\n".join(response)


# -------------------------------------
# БЛОК НОТАТОК (ПОВНІСТЮ СИНХРОНІЗОВАНО З MAIN.PY)
# -------------------------------------

@input_error
def add_note(args: list, notes: NoteBook) -> str:
    """
    Додає нотатку
    Приймає: [text...]
    """
    text = " ".join(args)
    if not text:
        raise ValueError("Note text cannot be empty.")
    note = Note(text)
    new_id = notes.add_note(note) 
    return f"{styles.SUCCESS}Нотатку додано (ID: {new_id})"

@input_error
def find_note(args: list, notes: NoteBook) -> str:
    """
    ❗️ НОВА ФУНКЦІЯ (Фікс "подивитися окрему")
    Показує ОДНУ нотатку за її ID.
    Приймає: [note_id]
    """
    try:
        note_id = int(args[0])
    except IndexError:
        return f"{styles.ERROR}Вкажіть ID нотатки."
    except ValueError:
        return f"{styles.ERROR}ID нотатки має бути числом."
        
    note = notes.find_by_id(note_id)
    if note is None:
        raise KeyError(f"Note with ID '{note_id}' not found.")
    
    return f"ID {note_id}: {str(note)}" # Повертаємо одну нотатку

@input_error
def show_notes(args: list, notes: NoteBook) -> str:
    """Показує всі нотатки (з їх ID)"""
    if not notes.data:
        return f"{styles.WARNING}Книга нотаток порожня."

    response = [f"{styles.SUCCESS}--- Всі Нотатки ---"]
    for note_id, note in notes.data.items():
        response.append(f"ID {note_id}: {str(note)}")
    return "\n".join(response)

@input_error
def edit_note_handler(args: list, notes: NoteBook) -> str:
    """
    ❗️ НОВА ФУНКЦІЯ (Фікс 'редагувати нотатку')
    Редагує текст нотатки за її ID.
    Приймає: [note_id] [новий текст...]
    """
    try:
        note_id = int(args[0])
    except IndexError:
        return f"{styles.ERROR}Вкажіять ID нотатки та новий текст."
    except ValueError:
        return f"{styles.ERROR}ID нотатки має бути числом."
    
    new_text = " ".join(args[1:])
    if not new_text:
        return f"{styles.ERROR}Вкажіть новий текст для нотатки."
    
    notes.edit_note(note_id, new_text) # Метод з models.py
    return f"{styles.SUCCESS}Нотатку {note_id} оновлено."

@input_error
def delete_note(args: list, notes: NoteBook) -> str:
    """
    Видаляє нотатку за ID
    Приймає: [note_id]
    """
    try:
        note_id = int(args[0])
    except IndexError:
        return f"{styles.ERROR}Вкажіть ID нотатки для видалення."
    except ValueError:
        return f"{styles.ERROR}ID нотатки має бути числом."
        
    notes.delete_note(note_id)
    return f"{styles.SUCCESS}Нотатку {note_id} видалено."

@input_error
def search_notes_handler(args: list, notes: NoteBook) -> str:
    """
    ❗️ ПЕРЕЙМЕНОВАНО (раніше була 'find_note')
    Пошук нотаток за текстом
    Приймає: [query...]
    """
    query = " ".join(args)
    if not query:
        return f"{styles.ERROR}Вкажіть текст для пошуку."
        
    found = notes.search_by_text(query)

    if not found:
        return f"{styles.WARNING}Не знайдено нотаток, що містять '{query}'."

    response = [f"{styles.SUCCESS}Нотатки, що відповідають запиту '{query}':"]
    # ❗️ Виправлено: 'str(note)' вже має 'ID' з 'NoteBook'
    for note in found:
        response.append(f"ID {note.id}: {str(note)}") 
    return "\n".join(response)

# --- (Обробники для Тегів) ---

@input_error
def add_tag(args: list, notes: NoteBook) -> str:
    """
    Додає теги до нотатки
    Приймає: [note_id] [tag1] [tag2] ...
    """
    try:
        note_id = int(args[0])
        tags = args[1:]
    except ValueError:
        return f"{styles.ERROR}ID нотатки має бути числом."
    except IndexError:
        raise ValueError("Вкажіть ID нотатки та хоча б один тег.")
        
    if not tags:
        raise ValueError("Вкажіть хоча б один тег.")

    note = notes.find_by_id(note_id) 
    if note is None:
        raise KeyError(f"Note with ID '{note_id}' not found.")

    added_tags = []
    for tag in tags:
        if note.add_tag(tag): # add_tag повертає True, якщо тег новий
            added_tags.append(tag)
            
    if not added_tags:
         return f"{styles.WARNING}Теги вже існують для нотатки {note_id}."
         
    return f"{styles.SUCCESS}Теги {added_tags} додано до нотатки {note_id}."

@input_error
def search_by_tag(args: list, notes: NoteBook) -> str:
    """
    ❗️ ПЕРЕЙМЕНОВАНО (раніше була 'find_tag')
    Пошук нотаток за тегом
    Приймає: [tag_query]
    """
    tag_query = " ".join(args)
    if not tag_query:
        return f"{styles.ERROR}Вкажіть тег для пошуку."
        
    found = notes.search_by_tag(tag_query)

    if not found:
        return f"{styles.WARNING}Не знайдено нотаток з тегом '{tag_query}'."

    response = [f"{styles.SUCCESS}Нотатки з тегом '{tag_query}':"]
    for note in found:
        response.append(f"ID {note.id}: {str(note)}")
    return "\n".join(response)


@input_error
def sort_notes_by_tags(args: list, notes: NoteBook) -> str:
    """
    Сортує та виводить нотатки за тегами
    """
    sorted_notes = notes.sort_by_tags()

    if not sorted_notes:
        return f"{styles.WARNING}Книга нотаток порожня, нічого сортувати."

    response = [f"{styles.SUCCESS}--- Нотатки, відсортовані за тегами ---"]
    for note in sorted_notes:
        response.append(f"ID {note.id}: {str(note)}")
    return "\n".join(response)

# ❗️ ОБОВ'ЯЗКОВО! Обробник для 'all'
@input_error
def show_all(book: AddressBook, notes: NoteBook) -> str:
    """
    Показує всі контакти ТА всі нотатки.
    """
    response = [f"{styles.SUCCESS}--- Всі Контакти ---"]
    if not book.data:
        response.append(f"{styles.WARNING}Адресна книга порожня.")
    else:
        for record in book.data.values():
            response.append(str(record))
    
    response.append(f"\n{styles.SUCCESS}--- Всі Нотатки ---")
    if not notes.data:
        response.append(f"{styles.WARNING}Книга нотаток порожня.")
    else:
        for note_id, note in notes.data.items():
            response.append(f"ID {note_id}: {str(note)}")
            
    return "\n".join(response)
