import sqlite3

class Repository:
    """Tang truy cap du lieu: chi lam viec voi SQL (truy van tham so hoa)."""
    def __init__(self, path=":memory:"):
        self.conn = sqlite3.connect(path)
        self.conn.execute("CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, title TEXT NOT NULL, author TEXT, qty INTEGER NOT NULL CHECK(qty>=0))")
        self.conn.execute("CREATE TABLE IF NOT EXISTS loans(id INTEGER PRIMARY KEY, book_id INTEGER NOT NULL, member TEXT NOT NULL)")

    def insert_book(self, title, author, qty):
        cur = self.conn.execute("INSERT INTO books(title,author,qty) VALUES(?,?,?)", (title, author, qty))
        self.conn.commit(); return cur.lastrowid

    def find_by_title(self, keyword):
        return self.conn.execute("SELECT id,title,author,qty FROM books WHERE title LIKE ?", (f"%{keyword}%",)).fetchall()

    def get_qty(self, book_id):
        row = self.conn.execute("SELECT qty FROM books WHERE id=?", (book_id,)).fetchone()
        return None if row is None else row[0]

    def add_loan(self, book_id, member):
        with self.conn:
            self.conn.execute("UPDATE books SET qty=qty-1 WHERE id=?", (book_id,))
            self.conn.execute("INSERT INTO loans(book_id,member) VALUES(?,?)", (book_id, member))

    def has_loan(self, book_id, member):
        return self.conn.execute("SELECT 1 FROM loans WHERE book_id=? AND member=?", (book_id, member)).fetchone() is not None

    def remove_loan(self, book_id, member):
        with self.conn:
            self.conn.execute("UPDATE books SET qty=qty+1 WHERE id=?", (book_id,))
            self.conn.execute("DELETE FROM loans WHERE id=(SELECT id FROM loans WHERE book_id=? AND member=? LIMIT 1)", (book_id, member))
