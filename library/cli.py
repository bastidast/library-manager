from .repository import Repository
from .service import LibraryService
from .errors import LibraryError

def main():
    svc = LibraryService(Repository())
    while True:
        c = input("1.Them 2.Tim 3.Muon 4.Tra 0.Thoat: ")
        try:
            if c == "1": svc.add_book(input("Ten: "), input("Tac gia: "), int(input("SL: ")))
            elif c == "2": print(svc.search(input("Tu khoa: ")))
            elif c == "3": svc.borrow(int(input("Ma sach: ")), input("Ten ban doc: "))
            elif c == "4": svc.return_book(int(input("Ma sach: ")), input("Ten ban doc: "))
            else: break
        except (LibraryError, ValueError) as e:
            print("Loi:", e)

if __name__ == "__main__":
    main()
