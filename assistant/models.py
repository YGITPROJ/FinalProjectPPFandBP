#
#
#
import re
from collections import UserDict
from datetime import datetime, date
import uuid


class Field:
    """
    Базовий клас для всіх полів.
    Ми використаємо getter'и та setter'и для доступу до value щоб реалізувати валідацію
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

    def get_upcoming_birthdays(self, days: int) -> list:  # ЗМІНЕНО: Приймає 'days'
        """
        Повертає список контактів, яких треба привітати
        протягом наступних 'days' днів, враховуючи вихідні
        """
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

            # Перевіряємо, чи день народження в межах заданого 'days'
            if 0 <= delta_days < days:
                weekday = bday_this_year.weekday()

                if weekday >= 5:
                    # Переносимо на понеділок
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


class Tag(Field):
    """Клас для тегів нотаток"""

    pass


class Note:
    """
    Клас для однієї нотатки.
    Містить унікальний ID, текст та список тегів
    """

    def __init__(self, text: str):
        self.id = str(uuid.uuid4())
        self.text = text
        self.tags = []
        self.created_at = datetime.now()

    def add_tag(self, tag_text: str):
        self.tags.append(Tag(tag_text))

    def remove_tag(self, tag_text: str):
        tag_to_remove = None
        for tag in self.tags:
            if tag.value == tag_text:
                tag_to_remove = tag
                break
        if tag_to_remove:
            self.tags.remove(tag_to_remove)
        else:
            raise ValueError(f"Tag '{tag_text}' not found.")

    def __str__(self):
        tags_str = ", ".join(t.value for t in self.tags)
        return (
            f"ID: {self.id}\n"
            f"Created: {self.created_at.strftime('%Y-%m-%d %H:%M')}\n"
            f"Tags: [{tags_str}]\n"
            f"Text: {self.text}\n"
            f"--------------------"
        )


class NoteBook(UserDict):
    """
    Monitor
        Клас для управління нотатками.
        Ми зберігаємо нотатки в словнику, де ключ - це ID нотатки
    """

    def add_note(self, note: Note):
        self.data[note.id] = note

    def find_by_id(self, note_id: str) -> Note:
        return self.data.get(note_id)

    def delete_note(self, note_id: str):
        if note_id in self.data:
            del self.data[note_id]
        else:
            raise KeyError(f"Note with ID '{note_id}' not found.")

    def search_by_text(self, query: str) -> list:
        """Пошук нотаток, що містять 'query' в тексті."""
        return [
            note for note in self.data.values() if query.lower() in note.text.lower()
        ]

    def search_by_tag(self, tag_query: str) -> list:
        """Пошук нотаток, що містять 'tag_query' в одному з тегів"""
        found_notes = []
        for note in self.data.values():
            for tag in note.tags:
                if tag_query.lower() in tag.value.lower():
                    found_notes.append(note)
                    break
        return found_notes

    def sort_by_tags(self) -> list:  # Бонусна функція
        """
        Сортує нотатки за кількістю тегів (та за алфавітом тегів)
        """
        # Сортуємо за алфавітом першого тега, якщо він є
        return sorted(
            self.data.values(),
            key=lambda note: note.tags[0].value.lower() if note.tags else "",
        )
