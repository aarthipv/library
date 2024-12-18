import json
from datetime import datetime

# File paths for books and users
BOOKS_FILE = 'books.json'
USERS_FILE = 'users.json'

# Load books data from JSON file
def load_books():
    try:
        with open(BOOKS_FILE, 'r') as file:
            books = json.load(file)
    except FileNotFoundError:
        books = []
    return books

# Save books data to JSON file
def save_books(books):
    with open(BOOKS_FILE, 'w') as file:
        json.dump(books, file, indent=4)

# Load user data from JSON file
def load_users():
    try:
        with open(USERS_FILE, 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []
    return users

# Save user data to JSON file
def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)

# Add a book to the system
def add_book():
    books = load_books()
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    isbn = input("Enter ISBN: ")
    
    # Check if the book already exists
    if any(book['isbn'] == isbn for book in books):
        print("Book already exists!")
        return

    book = {
        'isbn': isbn,
        'title': title,
        'author': author,
        'available': True
    }

    books.append(book)
    save_books(books)
    print("Book added successfully.")

# Remove a book from the system
def remove_book():
    books = load_books()
    isbn = input("Enter ISBN of the book to remove: ")
    books = [book for book in books if book['isbn'] != isbn]
    save_books(books)
    print("Book removed successfully.")

# Search books by title, author, or ISBN
def search_books():
    books = load_books()
    search_term = input("Enter title, author, or ISBN to search: ").lower()

    found_books = [book for book in books if (search_term in book['title'].lower()) or 
                   (search_term in book['author'].lower()) or 
                   (search_term in book['isbn'])]

    if found_books:
        for book in found_books:
            print(f"ISBN: {book['isbn']}, Title: {book['title']}, Author: {book['author']}, Available: {book['available']}")
    else:
        print("No books found matching your search.")

# Borrow a book
def borrow_book():
    users = load_users()
    books = load_books()

    user_id = input("Enter user ID: ")
    user = next((u for u in users if u['user_id'] == user_id), None)

    if not user:
        print("User not found.")
        return

    isbn = input("Enter ISBN of the book to borrow: ")
    book = next((b for b in books if b['isbn'] == isbn), None)

    if not book:
        print("Book not found.")
        return

    if not book['available']:
        print("Book is currently unavailable.")
        return

    book['available'] = False
    due_date = datetime.now().strftime("%Y-%m-%d")
    user['borrowed_books'].append({'isbn': isbn, 'due_date': due_date})

    save_books(books)
    save_users(users)
    print(f"Book borrowed. Due date: {due_date}")

# Return a borrowed book
def return_book():
    users = load_users()
    books = load_books()

    user_id = input("Enter user ID: ")
    user = next((u for u in users if u['user_id'] == user_id), None)

    if not user:
        print("User not found.")
        return

    isbn = input("Enter ISBN of the book to return: ")
    borrowed_book = next((b for b in user['borrowed_books'] if b['isbn'] == isbn), None)

    if not borrowed_book:
        print("This book was not borrowed by the user.")
        return

    book = next((b for b in books if b['isbn'] == isbn), None)
    book['available'] = True
    user['borrowed_books'] = [b for b in user['borrowed_books'] if b['isbn'] != isbn]

    save_books(books)
    save_users(users)
    print("Book returned successfully.")

# View all users
def view_users():
    users = load_users()
    if not users:
        print("No users found.")
        return
    for user in users:
        print(f"User ID: {user['user_id']}, Name: {user['name']}, Borrowed Books: {len(user['borrowed_books'])}")

# Main menu
def main_menu():
    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Search Books")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. View Users")
        print("7. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            add_book()
        elif choice == '2':
            remove_book()
        elif choice == '3':
            search_books()
        elif choice == '4':
            borrow_book()
        elif choice == '5':
            return_book()
        elif choice == '6':
            view_users()
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
