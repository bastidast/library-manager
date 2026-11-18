class LibraryError(Exception):
    """Loi nghiep vu chung."""
class ValidationError(LibraryError): pass
class OutOfStockError(LibraryError): pass
class NotBorrowedError(LibraryError): pass
