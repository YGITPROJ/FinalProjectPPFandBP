# **Personal Assistant (CLI)**

A comprehensive, command-line (CLI) personal assistant built with Python. This tool allows you to efficiently manage your contacts, address book, and personal notes directly from your terminal. All data is saved locally to your disk, ensuring privacy and fast access.

## **Features**

### **Contact Management**

- **Add Contact:** Create new contacts with a name, phone, email, birthday, and address.
- **Update Contact:** Add new phones or update the email, birthday, or address for an existing contact.
- **Show Contact:** Display all details for a single contact in a clean, tree-like structure.
- **Show All:** List all contacts in the address book.
- **Upcoming Birthdays:** Show a list of all contacts with birthdays in the next 'N' days (default is 7).

### **Note Management**

- **Add Note:** Create a new note with any text content.
- **Add Tags:** Add one or more tags to an existing note for categorization.
- **Show All Notes:** Display all notes with their IDs, creation dates, tags, and text.
- **Find Note by Text:** Search all notes for a specific word or phrase.
- **Find Note by Tag:** Find all notes matching a specific tag.
- **Sort Notes:** Display all notes sorted alphabetically by their first tag.
- **Delete Note:** Remove a note by its unique ID.

### **Other**

- **Data Persistence:** All contacts and notes are automatically saved to disk (in DB/assistant_data.pkl) on exit and reloaded on start.
- **Color-coded Interface:** Uses colorama for a more readable and user-friendly terminal experience.

## **Technologies Used**

- Python 3.x
- colorama (for styled terminal output)
- pickle (for data serialization and persistence)

## **Installation**

1. **Clone the repository:**  
   git clone \[https://github.com/YGITPROJ/FinalProjectPPFandBP.git\](https://github.com/YGITPROJ/FinalProjectPPFandBP.git)  
   cd FinalProjectPPFandBP

2. Install dependencies:  
   This project uses colorama for styling.  
   pip install colorama

## **Usage**

To run the assistant, execute the main.py file from the root directory:

python main.py

You will be greeted with a prompt. Type your commands and press Enter.

### **Available Commands**

**General**

- hello: Greet the bot.
- close / exit: Save data and exit the assistant.

**Contacts**

- add-contact \[name\] phone \[phone\] email \[email\] birthday \[dd.mm.yyyy\] address \[address...\]
  - _Example: add-contact John phone 1234567890 email john@example.com_
- update-contact \[name\] phone \[phone\] (adds a new phone)
- update-contact \[name\] email \[email\] (updates email)
- show-contact \[name\]
  - _Example: show-contact John_
- show-all
- birthdays \[days\]
  - _Example: birthdays 7_

**Notes**

- add-note \[text...\]
  - _Example: add-note My first note about Python_
- add-tag \[note_id\] \[tag1\] \[tag2...\]
  - _Example: add-tag \<note-id-from-show-notes\> python project_
- show-notes
- find-note \[query...\]
  - _Example: find-note Python_
- find-tag \[tag\]
  - _Example: find-tag project_
- sort-notes
- delete-note \[note_id\]

## **Project Structure**

Based on the imports, the project assumes the following structure:

personal-assistant/  
├── main.py \# Main entry point and command dispatcher  
├── DB/ \# Default directory for storing data (auto-created)  
│ └── assistant_data.pkl  
└── assistant/  
 ├── \_\_init\_\_.py  
 ├── models.py \# Core data classes (AddressBook, Record, NoteBook, Note)  
 ├── handlers.py \# Business logic for all user commands  
 ├── storage.py \# Handles saving and loading data (pickle)  
 ├── config.py \# Configuration (e.g., storage path)  
 └── styles.py \# Manages terminal colors (colorama)

## **Authors**

- (team members here)

## **License**

This project is licensed under the MIT License.
