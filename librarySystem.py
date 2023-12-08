import datetime

class Book:
    def __init__(self,id,title,author,quantity,available):
        self.id = id
        self.title = title
        self.author = author
        self.quantity = int(quantity)
        self.available = bool(available )

    def display_details(self):
       return f"{self.id}. Title:  {self.title}\nAuthor:  {self.author}\nAvailable:  {self.available}"
    def checkout_quantity(self, quantity):
        self.quantity -= quantity
        if self.quantity < 0:
            self.quantity = 0
            self.checkout_available()
    def return_quantity(self, quantity):
        self.quantity += quantity
        self.return_available()
            
    def checkout_available(self):
        if self.quantity == 0:
            self.available = False
    def return_available(self):
        if self.quantity > 0:
            self.available = True
class Library:

    def __init__(self, file_path) :
        self.books = {}
        self.load_books(file_path)

    def display_catalog(self):
        print("BOOK'S CATALOG:\n")
        for book in self.books.values():
            print(f"{book.display_details()}\n")

    def load_books(self, file_path):
        with open(file_path,"r") as file:
            id = 1
            for line in file:
                info = line.split("-")
                self.books[id]=Book(id,info[0],info[1],info[2],info[3])
                id += 1
    def return_id(self):
        return self.books.keys()

    def check_available(self, id, quantity):
        book = self.books[int(id)]
        if not book.available or quantity> book.quantity:
            print(f"Error: {quantity} copies of {book.title} not available.")
            return None
        elif quantity > 0:
            return quantity
    
    def calculate_due_date(self):
        date = datetime.datetime.now()+ datetime.timedelta(days=14)
        return date.strftime("%x")
    
    def validate_due_date(self,date):
        try:
            date = [int(i) for i in date.split("-")]
            return datetime.datetime(date[0],date[1],date[2])
        except:
            return None


def main():
    library = Library("books.txt")
    op = ""
    while op != "4":
        print("1. Display Catalog")
        print("2. Checkout Books")
        print("3. Return Books")
        print("4. Exit")

        op = input("Enter an option (1-4): ")

        if op == "1":
            library.display_catalog()
        elif op == "2":
            sel_books = {}
            quantity_books = 0
            book_id = "0"
            while book_id.isdigit():
                book_id = input("Enter the number of the book to checkout (stop to end the selection): ")
                if book_id.lower() == "stop":
                    break
                elif int(book_id) not in library.return_id():
                    print(f"Error: Book '{book_id}' not found in the catalog.")
                    
                book = library.books[int(book_id)]
                quantity =input(f"Enter the quantity for {book.title}: ")
                if quantity.isdigit() and quantity != "0":
                    quantity = library.check_available(book_id,int(quantity))
                else:
                    print(f"Error: {quantity} copies of {book.title} not available.")
                    continue
                if quantity is not None:
                    sel_books[book] = {"quantity":quantity,"due_date":library.calculate_due_date()}
                    book.checkout_quantity(quantity)
                    library.books[int(book_id)] = book
                    quantity_books += quantity
                elif quantity_books >10:
                    print("Error: You exceed more than 10 books in a single transaction.")
                    return -1
                else:
                    continue
     
           

        elif op == "3":
            library.display_catalog()
            book_id = "0"
            late_fee = 0
            while book_id.isdigit():
                book_id = input("Enter the number of the book to return (stop to end the return): ")
                if book_id.lower() == "stop":
                    return -1
                elif int(book_id) not in library.return_id():
                    print(f"Error: Book '{book_id}' not found in the catalog.")

                book = library.books[int(book_id)]
                quantity = input(f"Enter the quantity for {book.title}: ")
                if quantity.isdigit():
                    book.return_quantity(int(quantity))
                    library.books[int(book_id)] = book
                else:
                    print("Error: The quantity is not correct")
                due_date = input("Enter the due date of the book(YYYY-MM-DD): ")
                due_date = library.validate_due_date(due_date)
                if due_date is not None:
                    day_dif = (due_date - datetime.datetime.now()).days()
                    if day_dif >= 0:
                        print("The book don't have late fee")
                        continue
                    else:
                        late_fee += quantity * abs(day_dif)
                else:
                    print("Error: The date input is not correctcly.")

            print(f"\nReturn successful! Total late fees: ${late_fee}")           


        elif op == "4":
            print("Thanks! See you soon")

        else:
            print("Invalid option. Please the option between 1 and 4.")

    

if __name__ == "__main__":
    main()

