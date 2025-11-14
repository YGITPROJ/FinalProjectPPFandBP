#
#
#
import re
from collections import UserDict
from datetime import datetime, date


class Field:
    """
    Базовий клас для всіх полів
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
            raise ValueError("Ім'я не може бути порожнім.")
        self._value = new_value


class Phone(Field):
    """Клас для зберігання номера телефону"""

    @Field.value.setter
    def value(self, new_value):
        if not (len(new_value) == 10 and new_value.isdigit()):
            raise ValueError("Невірний номер телефону: має бути 10 цифр.")
        self._value = new_value


class Birthday(Field):
    """Клас для зберігання дня народження"""

    @Field.value.setter
    def value(self, new_value: str):
        try:
            parsed_date = datetime.strptime(new_value, "%d.%m.%Y").date()
            self._value = parsed_date
        except ValueError:
            raise ValueError("Невірний формат дати. Використовуйте DD.MM.YYYY")

    def __str__(self):
        return self._value.strftime("%d.%m.%Y")


class Email(Field):
    """Клас для зберігання email"""

    @Field.value.setter
    def value(self, new_value: str):
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", new_value):
            raise ValueError("Невірний формат email.")
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
        self.phone = None
        self.email = None
        self.address = None
        self.birthday = None

    def add_phone(self, phone_number: str):
        self.phone = Phone(phone_number)

    def add_birthday(self, birthday_str: str):
        self.birthday = Birthday(birthday_str)

    def add_email(self, email_str: str):
        self.email = Email(email_str)

    def add_address(self, address_str: str):
        self.address = Address(address_str)

    def __str__(self):
        parts = []
        if self.phone:
            parts.append(f"phone: {self.phone}")
        if self.email:
            parts.append(f"email: {self.email}")
        if self.address:
            parts.append(f"address: {self.address}")
        if self.birthday:
            parts.append(f"birthday: {self.birthday}")

        data_str = ", ".join(parts)
        if not data_str:
            data_str = "Немає додаткових даних."

        return f"Контакт: {self.name.value} [{data_str}]"


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
            raise KeyError(f"Контакт '{name}' не знайдено.")

    def get_upcoming_birthdays(self, days: int, reference_date: date = None) -> list:
        today = reference_date if reference_date is not None else date.today()

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

    def search(self, query: str) -> list[Record]:
        found_records = []
        query_lower = query.lower()

        for record in self.data.values():
            fields_to_check = [
                record.name,
                record.phone,
                record.email,
                record.address,
                record.birthday,
            ]

            for field in fields_to_check:
                if field is not None:
                    if query_lower in str(field).lower():
                        found_records.append(record)
                        break

        return found_records


class Tag(Field):
    """Клас для тегів нотаток"""

    pass


class Note:
    """
    Клас для однієї нотатки.
    """

    def __init__(self, text: str):
        self.id = None  # ID присвоюється NoteBook
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
            raise ValueError(f"Тег '{tag_text}' не знайдено.")

    def update_text(self, new_text: str):
        """Оновлює текст нотатки."""
        if not new_text:
            raise ValueError("Текст нотатки не може бути порожнім.")
        self.text = new_text

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
    Клас для управління нотатками.
    Ключ - це простий числовий ID.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # _next_id буде ініційовано при першому додаванні,
        # якщо об'єкт завантажено з pickle і він вже має дані
        if hasattr(self, "data") and self.data:
            # Відновлюємо лічильник з максимального існуючого ключа
            self._next_id = max(self.data.keys()) + 1
        else:
            # Починаємо з 1 для нової книги
            self._next_id = 1

    def add_note(self, note: Note) -> int:
        """
        Додає нотатку, присвоює їй наступний доступний ID і повертає цей ID
        """
        note_id = self._next_id
        note.id = note_id
        self.data[note_id] = note
        self._next_id += 1
        return note_id

    def find_by_id(self, note_id_str: str) -> Note:
        """
        Знаходить нотатку за її числовим ID (який передається у вигляді рядка)
        """
        try:
            note_id = int(note_id_str)
            return self.data.get(note_id)
        except (ValueError, TypeError):
            return None

    def delete_note(self, note_id_str: str):
        """
        Видаляє нотатку за її числовим ID (який передається у вигляді рядка)
        """
        try:
            note_id = int(note_id_str)
            if note_id in self.data:
                del self.data[note_id]
            else:
                raise KeyError(f"Нотатку з ID '{note_id}' не знайдено.")
        except (ValueError, TypeError):
            raise KeyError(f"Невірний ID: '{note_id_str}'. Потрібно число.")

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

    def sort_by_tags(self) -> list:
        """
        Сортує нотатки за алфавітом першого тега
        """
        return sorted(
            self.data.values(),
            key=lambda note: note.tags[0].value.lower() if note.tags else "",
        )
