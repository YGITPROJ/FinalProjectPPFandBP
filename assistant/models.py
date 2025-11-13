#
# === Твій models.py (ВИПРАВЛЕНО БЛОК НОТАТОК) ===
#
import re
from collections import UserDict
from datetime import datetime, date
# ❗️ 'uuid' нам більше не потрібен!
# import uuid 

# -------------------------------------
# БЛОК КОНТАКТІВ (Я НЕ ЧІПАВ ЦЕЙ КОД)
# -------------------------------------

class Field:
    """
    Базовий клас для всіх полів.
    """
    def __init__(self, value):
        self.value = value
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, new_value):
        self._value = new_value
    def __str__(self):
        return str(self._value)

class Name(Field):
    """Клас для зберігання імені"""
    @Field.value.setter
    def value(self, new_value):
        if not new_value:
            raise ValueError("Name cannot be empty.")
        self._value = new_value

class Phone(Field):
    """Клас для зберігання номера телефону"""
    @Field.value.setter
    def value(self, new_value):
        if not (len(new_value) == 10 and new_value.isdigit()):
            raise ValueError("Invalid phone number: must be 10 digits.")
        self._value = new_value

class Birthday(Field):
    """Клас для зберігання дня народження"""
    @Field.value.setter
    def value(self, new_value: str):
        try:
            parsed_date = datetime.strptime(new_value, "%d.%m.%Y").date()
            self._value = parsed_date
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
    def __str__(self):
        return self._value.strftime("%d.%m.%Y")

class Email(Field):
    """Клас для зберігання email"""
    @Field.value.setter
    def value(self, new_value: str):
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", new_value):
            raise ValueError("Invalid email format.")
        self._value = new_value

class Address(Field):
    """Клас для зберігання адреси"""
    pass

class Record:
    """
    Клас для зберігання одного запису (контакту)
    """
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.address = None
        self.birthday = None
    # ... (всі твої методи 'add_phone', 'remove_phone', ... 'add_address' ... )
    def add_phone(self, phone_number: str):
        self.phones.append(Phone(phone_number))
    def remove_phone(self, phone_number: str):
        phone_to_remove = self.find_phone(phone_number)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError(f"Phone number {phone_number} not found.")
    def edit_phone(self, old_phone_number: str, new_phone_number: str):
        phone_to_edit = self.find_phone(old_phone_number)
        if phone_to_edit:
            phone_to_edit.value = new_phone_number
        else:
            raise ValueError(f"Phone number {old_phone_number} not found.")
    def find_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None
    def add_birthday(self, birthday_str: str):
        self.birthday = Birthday(birthday_str)
    def add_email(self, email_str: str):
        self.email = Email(email_str)
    def add_address(self, address_str: str):
        self.address = Address(address_str)
    def __str__(self):
        phone_list = "; ".join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        email_str = f", email: {self.email}" if self.email else ""
        address_str = f", address: {self.address}" if self.address else ""
        return (
            f"Contact name: {self.name.value}, "
            f"phones: {phone_list}{email_str}{address_str}{birthday_str}"
        )

class AddressBook(UserDict):
    """Клас для управління адресною книгою"""
    def add_record(self, record: Record):
        self.data[record.name.value] = record
    def find(self, name: str) -> Record:
        return self.data.get(name)
    def delete(self, name: str):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Contact '{name}' not found.")
    def get_upcoming_birthdays(self, days: int) -> list:
        # ... (твій код 'get_upcoming_birthdays') ...
        today = date.today()
        upcoming_birthdays = []
        for record in self.data.values():
            if not record.birthday:
                continue
            bday = record.birthday.value
            bday_this_year = bday.replace(year=today.year)
            if bday_this_year < today:
                bday_this_year = bday.replace(year=today.year + 1)
            delta_days = (bday_this_year - today).days
            if 0 <= delta_days < days:
                weekday = bday_this_year.weekday()
                if weekday >= 5:
                    day_to_congratulate = bday_this_year.strftime("%A (%A in fact)")
                else:
                    day_to_congratulate = bday_this_year.strftime("%A")
                upcoming_birthdays.append(
                    {
                        "name": record.name.value,
                        "congratulation_day": day_to_congratulate,
                        "birthday_date": str(record.birthday),
                    }
                )
        return upcoming_birthdays

# -------------------------------------
# БЛОК НОТАТОК (ПОВНІСТЮ ЗАМІНЕНО)
# -------------------------------------

class Tag(Field):
    """Клас для тегів нотаток"""
    pass


class Note:
    """
    Клас для однієї нотатки.
    ❗️ ФІКС: ID тепер призначається 'NoteBook'
    """
    def __init__(self, text: str):
        # ❗️ ФІКС: 'uuid' видалено. 
        self.id = None # ID буде призначено 'NoteBook'
        self.text = text
        self.tags = []
        self.created_at = datetime.now()

    # ❗️ НОВИЙ МЕТОД (Вимога 8: Редагувати)
    def edit_text(self, new_text: str):
        self.text = new_text # Просто замінюємо текст

    # ❗️ Покращення: перевірка на дублікати тегів
    def add_tag(self, tag_text: str):
        if not self.find_tag(tag_text):
            self.tags.append(Tag(tag_text))
            return True
        return False # Такий тег вже є

    def remove_tag(self, tag_text: str):
        tag_to_remove = self.find_tag(tag_text)
        if tag_to_remove:
            self.tags.remove(tag_to_remove)
        else:
            raise ValueError(f"Tag '{tag_text}' not found.")
    
    # Допоміжний метод для пошуку тегу
    def find_tag(self, tag_text: str):
        for tag in self.tags:
            # Пошук без урахування регістру
            if tag.value.lower() == tag_text.lower():
                return tag
        return None

    def __str__(self):
        # 'handler' буде показувати ID
        tags_str = ", ".join(t.value for t in self.tags)
        # ❗️ Я змінив .text на .text.value, щоб уникнути
        # показу <__main__.NoteText object ...>
        return (
            f"Created: {self.created_at.strftime('%Y-%m-%d %H:%M')}\n"
            f"Tags: [{tags_str}]\n"
            f"Text: {self.text.value if isinstance(self.text, Field) else self.text}\n" 
            f"--------------------"
        )


class NoteBook(UserDict):
    """
    Клас для управління нотатками.
    ❗️ ФІКС: Тепер веде лічильник 'next_id' (1, 2, 3...)
    """
    
    def __init__(self):
        super().__init__()
        # ❗️ ФІКС (Проблема №2: "дренючі ID")
        self.next_id = 1 
        # (Тут буде логіка відновлення next_id при завантаженні)
        
    def load_fix_next_id(self):
        # ❗️ Допоміжний метод, який 'storage' має викликати
        # після завантаження, щоб ID не починались з 1 знову
        if self.data:
            # Знаходимо максимальний ID і ставимо next_id+1
            self.next_id = max(self.data.keys()) + 1

    # ❗️ ФІКС (Вимога 6: Зберігати)
    def add_note(self, note: Note):
        note_id = self.next_id
        note.id = note_id         # Призначаємо ID самій нотатці
        self.data[note_id] = note # Ключ - це 'int' (1, 2, 3...)
        
        self.next_id += 1 # Готуємо наступний ID
        
        # Повертаємо ID, як очікує 'handler'
        return note_id 

    # ❗️ ФІКС (Проблема №1: Подивитись окрему)
    def find_by_id(self, note_id: int) -> Note:
        # 'note_id' тепер 'int'
        return self.data.get(note_id)

    # ❗️ НОВИЙ МЕТОД (Вимога 8: Редагувати)
    def edit_note(self, note_id: int, new_text: str):
        note = self.find_by_id(note_id)
        if note:
            note.edit_text(new_text)
        else:
            raise KeyError(f"Note with ID '{note_id}' not found.")

    # ❗️ ФІКС (Вимога 8: Видаляти)
    def delete_note(self, note_id: int):
        # 'note_id' тепер 'int'
        if note_id in self.data:
            del self.data[note_id]
        else:
            raise KeyError(f"Note with ID '{note_id}' not found.")

    # ❗️ ФІКС (Вимога 7: Пошук за текстом)
    def search_by_text(self, query: str) -> list:
        # (Код твоєї команди)
        # ❗️ Я виправив 'note.text' на 'note.text.value'
        return [
            note for note in self.data.values() if query.lower() in note.text.value.lower()
        ]

    # ❗️ ФІКС (Вимога 7: Пошук за тегом)
    def search_by_tag(self, tag_query: str) -> list:
        # (Код твоєї команди, трохи покращений)
        found_notes = []
        query_lower = tag_query.lower() 
        for note in self.data.values():
            if note.find_tag(query_lower): 
                found_notes.append(note)
        return found_notes

    # ❗️ ФІКС (Бонус 2: Сортування)
    def sort_by_tags(self) -> list:
        # (Код твоєї команди)
        return sorted(
            self.data.values(),
            key=lambda note: note.tags[0].value.lower() if note.tags else "",
        )