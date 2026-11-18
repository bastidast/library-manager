import unittest
from library.repository import Repository
from library.service import LibraryService
from library.errors import ValidationError, OutOfStockError, NotBorrowedError

class T(unittest.TestCase):
    def setUp(self):
        self.s = LibraryService(Repository())
        self.b = self.s.add_book("Clean Code", "R. Martin", 2)
    def test_tc1_add(self): self.assertEqual(self.s.qty_of(self.b), 2)
    def test_tc2_search(self): self.assertEqual(len(self.s.search("Clean")), 1)
    def test_tc3_borrow(self):
        self.s.borrow(self.b, "An"); self.assertEqual(self.s.qty_of(self.b), 1)
    def test_tc4_return(self):
        self.s.borrow(self.b, "An"); self.s.return_book(self.b, "An"); self.assertEqual(self.s.qty_of(self.b), 2)
    def test_tc5_out_of_stock(self):
        c = self.s.add_book("Hiem", "X", 1); self.s.borrow(c, "A")
        with self.assertRaises(OutOfStockError): self.s.borrow(c, "B")
        self.assertEqual(self.s.qty_of(c), 0)
    def test_tc6_negative_qty(self):
        with self.assertRaises(ValidationError): self.s.add_book("Sai", "Y", -5)
    def test_tc7_empty_title(self):
        with self.assertRaises(ValidationError): self.s.add_book("  ", "Y", 1)
    def test_tc8_sql_injection(self): self.assertEqual(len(self.s.search("zzz' OR 1=1 --")), 0)
    def test_tc9_return_not_borrowed(self):
        with self.assertRaises(NotBorrowedError): self.s.return_book(self.b, "Nobody")
    def test_borrow_missing_book(self):
        with self.assertRaises(ValidationError): self.s.borrow(999, "A")
    def test_two_members_borrow_same_book(self):
        self.s.borrow(self.b, "An"); self.s.borrow(self.b, "Binh"); self.assertEqual(self.s.qty_of(self.b), 0)
    def test_search_no_result(self): self.assertEqual(self.s.search("khong co"), [])

if __name__ == "__main__":
    unittest.main()
