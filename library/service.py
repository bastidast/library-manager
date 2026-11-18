from .errors import ValidationError, OutOfStockError, NotBorrowedError

class LibraryService:
    """Tang nghiep vu: kiem tra rang buoc, khong biet gi ve SQL hay giao dien."""
    def __init__(self, repo):
        self.repo = repo

    def add_book(self, title, author, qty):
        if not title or not title.strip():
            raise ValidationError("Ten sach khong duoc rong")
        if not isinstance(qty, int) or qty < 0:
            raise ValidationError("So luong phai la so nguyen >= 0")
        return self.repo.insert_book(title.strip(), author, qty)

    def search(self, keyword):
        return self.repo.find_by_title(keyword)

    def borrow(self, book_id, member):
        qty = self.repo.get_qty(book_id)
        if qty is None:
            raise ValidationError("Sach khong ton tai")
        if qty <= 0:
            raise OutOfStockError("Sach da het")
        self.repo.add_loan(book_id, member)

    def return_book(self, book_id, member):
        if not self.repo.has_loan(book_id, member):
            raise NotBorrowedError("Ban doc chua muon sach nay")
        self.repo.remove_loan(book_id, member)

    def qty_of(self, book_id):
        return self.repo.get_qty(book_id)
