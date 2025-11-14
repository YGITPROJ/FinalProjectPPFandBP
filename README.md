# **Personal Assistant (CLI)**

A comprehensive, command-line (CLI) personal assistant built with Python. This tool allows you to efficiently manage your contacts, address book, and personal notes directly from your terminal.

It features a robust command parser that understands quoted arguments (e.g., for names or addresses) and uses keyword flags (like -n for name, -p for phone) for a clear and flexible user experience.

## **Features**

### **Contact Management**

- **Add Contact:** Create new contacts with a name (-n), phone (-p), email (-e), birthday (-b), and address (-a).
- **Update Contact:** Update any field for an existing contact using their name (-n).
- **Show Contact:** Display all details for a single contact in a clean, tree-like structure.
- **Show All:** List all contacts in the address book.
- **Find Contact:** Search all contact fields (name, phone, email, etc.) for a matching query.
- **Upcoming Birthdays:** Show a list of contacts with birthdays in the next 'N' days. You can also specify a custom start date with the -d flag.

### **Note Management**

- **Add Note:** Create a new note. The app will assign it a simple integer ID.
- **Add Tags:** Add one or more tags to an existing note for categorization.
- **Show All Notes:** Display all notes, sorted by their ID.
- **Find Note by Text:** Search all notes for a specific word or phrase.
- **Find Note by Tag:** Find all notes matching a specific tag.
- **Sort Notes:** Display all notes sorted alphabetically by their first tag.
- **Delete Note:** Remove a note by its unique ID.

### **Other**

- **Data Persistence:** All contacts and notes are automatically saved to disk (in DB/assistant_data.pkl) on exit and reloaded on start.
- **Color-coded Interface:** Uses colorama for a more readable and user-friendly terminal experience.
- **Detailed Help:** A help command provides a full list of all commands, their syntax, and examples.

## **Technologies Used**

- Python 3.x
- colorama (for styled terminal output)
- pickle (for data serialization and persistence)

## **Installation**

1. **Clone the repository:**  
   git clone \[https://github.com/YGITPROJ/FinalProjectPPFandBP.git\]
   cd FinalProjectPPFandBP

2. **Install dependencies:**
   This project uses colorama for styling.  
   pip install colorama

## **Usage**

To run the assistant, execute the main.py file from the root directory:

python main.py

You will be greeted with a prompt. Type help to see all available commands.

### **Available Commands**

**General**

- hello: Greet the bot.
- help: Show the detailed help message.
- close / exit: Save data and exit the assistant.

**Contacts**

- add-contact -n [Name] [-p Phone] [-e Email] [-b DD.MM.YYYY] [-a Address]
  _Example: add-contact -n "John Doe" -p 1234567890 -e john@example.com_

- update-contact -n [Name] [-p Phone] [-e Email] [-b DD.MM.YYYY] [-a Address]
  _Example: update-contact -n "John Doe" -e new.email@example.com_

- show-contact [Name]
  _Example: show-contact "John Doe"_

- show-all

- find-contact [Query]
  _Example: find-contact John_

- birthdays [N] [-d DD.MM.YYYY]
  _Example 1: birthdays 10 (Show birthdays for the next 10 days from today)_
  _Example 2: birthdays -d 01.01.2025 (Show birthdays for the next 7 days from Jan 1st, 2025)_
  _Example 3: birthdays 15 -d 01.01.2025_

**Notes**

- add-note [Text...]
  _Example: add-note My first note about Python_

- update-note [ID] [New text...]
  _Example: update-note 1 This is the updated text._

- add-tag [ID] [tag1] [tag2...]
  _Example: add-tag 1 python project_

- show-notes

- find-note [Query...]
  _Example: find-note Python_

- find-tag [Tag]
  _Example: find-tag project_

- sort-notes

- delete-note [ID]

## **Project Structure**

Based on the imports, the project assumes the following structure:

personal-assistant/
├── main.py # Main entry point and command dispatcher
├── requirements.txt # Project dependencies
├── DB/ # Default directory for storing data (auto-created)
│ └── assistant_data.pkl
└── assistant/
├── **init**.py
├── models.py # Core data classes (AddressBook, Record, NoteBook, Note)
├── handlers.py # Business logic for all user commands
├── storage.py # Handles saving and loading data (pickle)
├── config.py # Configuration (e.g., storage path)
└── styles.py # Manages terminal colors (colorama)

## **Authors**

- Team Lead: YGITPROJ
- Team: andrii-jack, danavykhovanets-hub, portalinlife-hue, svetazo060510

## **License**

This project is licensed under the MIT License.
