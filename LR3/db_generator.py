import sqlite3
import os
import random
from datetime import datetime, timedelta

DB_NAME = "library.db"

def generate_database():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE books (
        id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER)''')
    cursor.execute('''CREATE TABLE readers (
        id INTEGER PRIMARY KEY, name TEXT, email TEXT)''')
    cursor.execute('''CREATE TABLE loans (
        id INTEGER PRIMARY KEY, book_id INTEGER, reader_id INTEGER, loan_date TEXT,
        FOREIGN KEY(book_id) REFERENCES books(id), FOREIGN KEY(reader_id) REFERENCES readers(id))''')

    books_data = [
        (1, "Война и мир", "Лев Толстой", 1869),
        (2, "Преступление и наказание", "Фёдор Достоевский", 1866),
        (3, "Мастер и Маргарита", "Михаил Булгаков", 1967),
        (4, "1984", "Джордж Оруэлл", 1949),
        (5, "Гарри Поттер и философский камень", "Джоан Роулинг", 1997),
        (6, "Евгений Онегин", "Александр Пушкин", 1833),
        (7, "Отцы и дети", "Иван Тургенев", 1862),
        (8, "Собачье сердце", "Михаил Булгаков", 1925),
        (9, "Три товарища", "Эрих Мария Ремарк", 1936),
        (10, "Маленький принц", "Антуан де Сент-Экзюпери", 1943),
        (11, "Портрет Дориана Грея", "Оскар Уайльд", 1890),
        (12, "Анна Каренина", "Лев Толстой", 1877),
        (13, "Идиот", "Фёдор Достоевский", 1869),
        (14, "Шерлок Холмс", "Артур Конан Дойл", 1887),
        (15, "Властелин колец", "Джон Толкин", 1954),
        (16, "Над пропастью во ржи", "Джером Сэлинджер", 1951),
        (17, "Мёртвые души", "Николай Гоголь", 1842),
        (18, "Герой нашего времени", "Михаил Лермонтов", 1840),
        (19, "О дивный новый мир", "Олдос Хаксли", 1932),
        (20, "Дюна", "Фрэнк Герберт", 1965)
    ]
    cursor.executemany("INSERT INTO books VALUES (?, ?, ?, ?)", books_data)

    readers_data = [
        (1, "Иванов Иван", "ivanov@mail.ru"),
        (2, "Смирнова Анна", "anna.s@mail.ru"),
        (3, "Кузнецов Дмитрий", "dmitry.k@mail.ru"),
        (4, "Попова Елена", "elena.p@mail.ru"),
        (5, "Соколов Алексей", "alex.s@mail.ru"),
        (6, "Лебедева Мария", "maria.l@mail.ru"),
        (7, "Козлов Сергей", "sergey.k@mail.ru"),
        (8, "Новикова Ольга", "olga.n@mail.ru"),
        (9, "Морозов Андрей", "andrey.m@mail.ru"),
        (10, "Волкова Татьяна", "tatiana.v@mail.ru")
    ]
    cursor.executemany("INSERT INTO readers VALUES (?, ?, ?)", readers_data)

    loans = []
    for i in range(1, 51):
        book_id = random.randint(1, 20)
        reader_id = random.randint(1, 10)
        days_ago = random.randint(0, 365)
        loan_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        loans.append((i, book_id, reader_id, loan_date))
    cursor.executemany("INSERT INTO loans VALUES (?, ?, ?, ?)", loans)

    conn.commit()
    conn.close()
    print(f"База '{DB_NAME}' создана.")

if __name__ == "__main__":
    generate_database()