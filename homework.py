import pickle
from datetime import datetime, timedelta



class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be a 10-digit number")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phone_str = "; ".join(str(p) for p in self.phones)
        if self.birthday:
            return f"Contact name: {self.name}, phones: {phone_str}, birthday: {self.birthday}"
        else:
            return f"Contact name: {self.name}, phones: {phone_str}"

class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.now().date()
        upcoming_week = today + timedelta(days=7)
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday:
                if record.birthday.value.date() >= today and record.birthday.value.date() <= upcoming_week:
                    upcoming_birthdays.append(record)
        return upcoming_birthdays

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"Error: {str(e)}"
    return wrapper

# Функції обробники команд
@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added for {name}."
    else:
        return f"Contact {name} not found."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday is {record.birthday}."
    elif record and not record.birthday:
        return f"{name} doesn't have a birthday set."
    else:
        return f"Contact {name} not found."

@input_error
def birthdays(args, book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "\n".join([f"{record.name}'s birthday on {record.birthday.value.strftime('%d.%m.%Y')}" for record in upcoming_birthdays])
    else:
        return "No upcoming birthdays."
    

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()   

# Основна програма
def main():
    book = load_data()  # Завантаження даних при запуску програми
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = user_input.split()

        if command in ["close", "exit"]:
            save_data(book)  # Збереження даних перед виходом з програми
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            name, phone = args
            record = book.find(name)
            if record:
                record.add_phone(phone)
                print("Phone number added/updated.")
            else:
                record = Record(name)
                record.add_phone(phone)
                book.add_record(record)
                print("Contact added.")

        elif command == "change":
            name, phone = args
            record = book.find(name)
            if record:
                record.edit_phone(phone)
                print("Phone number updated.")
            else:
                print(f"Contact {name} not found.")

        elif command == "phone":
            name = args[0]
            record = book.find(name)
            if record:
                print(f"Phone number(s) for {name}:")
                for phone in record.phones:
                    print(phone)
            else:
                print(f"Contact {name} not found.")

        elif command == "all":
            if book.data:
                print("All contacts:")
                for record in book.data.values():
                    print(record)
            else:
                print("No contacts in the address book.")

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
