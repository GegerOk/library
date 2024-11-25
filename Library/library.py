import sqlite3
import json
import os

db = sqlite3.connect('library.db')
c = db.cursor()


c.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER NOT NULL,
        status TEXT NOT NULL CHECK(status IN ('в наличии', 'выдана'))
    )
''')
db.commit()

# Добавление книги с указанием названи, автора, года


def add_book(title, author, year):
    c.execute('INSERT INTO books (title, author, year, status) VALUES (?, ?, ?, ?)',
              (title, author, year, 'в наличии'))
    db.commit()

# Удаление книги по id


def remove_book(book_id):
    c.execute('DELETE FROM books WHERE id = ?', (book_id,))
    if c.rowcount == 0:  # Проверяем, была ли затронута хотя бы одна строка
        print(f"Книга с ID {book_id} не найдена.")
        return 0
    else:
        db.commit()  # Подтверждаем изменения только если книга была удалена
        print(f"Книга с ID {book_id} была успешно удалена.")

# Поиск книги по названию или автору или году


def search_books(search_term):
    c.execute('SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR year = ?',
              (f'%{search_term}%', f'%{search_term}%', search_term))
    return c.fetchall()

# Отображение всех книг


def display_books():
    c.execute('SELECT * FROM books')
    return c.fetchall()

# Изменение статуса по id


def update_status(book_id, new_status):
    c.execute('UPDATE books SET status = ? WHERE id = ?',
              (new_status, book_id))
    db.commit()

# Функция которая автоматом при выходе конвертирует и сохраняет в .json


def export_to_json(filename):
    c.execute('SELECT * FROM books')
    books = c.fetchall()

# Конвертация
    books_list = []
    for book in books:
        books_list.append({
            'id': book[0],
            'title': book[1],
            'author': book[2],
            'year': book[3],
            'status': book[4]
        })

# Сохранение
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(books_list, f, indent=4, ensure_ascii=False)
    print(f"Данные успешно экспортированы в {filename}.")


# Основная функция при запуске программы
def main():
    while True:
        print("\n1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выход и сохранение в .json")
        choice = input("Выберите опцию: ")
        if choice == '1':
            title = input("Введите название книги: ")
            while len(title) > 100:
                title = input(
                    "Таких длинных книг не бывает, попробуй ещё раз ")
            author = input("Введите автора книги: ")
            while len(author) > 100:
                author = input(
                    "Таких длинных имён\фамилий не бывает, попробуй ещё раз ")
            year = int(input("Введите год издания книги: "))
            while year > 2024:
                year = input(
                    "Ещё не наступило, ещё раз ")
            add_book(title, author, year)
            print("Книга добавлена.")
        elif choice == '2':
            book_id = int(input("Введите ID книги для удаления: "))
            remove_book(book_id)
            if book_id == 0:
                print("Книга удалена.")
        elif choice == '3':
            search_term = input("Введите название, автора или год: ")
            results = search_books(search_term)
            print("Результаты поиска:")
            for book in results:
                print(book)
        elif choice == '4':
            books = display_books()
            print("Список всех книг:")
            for book in books:
                print(book)
        elif choice == '5':
            book_id = int(input("Введите ID книги для изменения статуса: "))
            new_status = input(
                "Введите новый статус ('в наличии' или 'выдана'): ")
            update_status(book_id, new_status)
            print("Статус книги изменен.")
        elif choice == '6':
            export_to_json('books_export.json')
            print("Выход...")
            break
        else:
            print("Неверный выбор! Попробуйте снова.")


if __name__ == "__main__":
    main()


db.close()
