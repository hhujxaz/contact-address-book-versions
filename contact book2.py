import csv

FILE_NAME = "contacts.csv"

# ========= Base Class =========
class Contact:
    def __init__(self, name, phone, email, address):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

    def to_list(self, ctype="General"):
        return [self.name, self.phone, self.email, self.address, ctype]


# ========= Child Classes =========
class PersonalContact(Contact):
    def to_list(self):
        return super().to_list("Personal")


class BusinessContact(Contact):
    def to_list(self):
        return super().to_list("Business")


# ========= Manager Class =========
class AddressBook:
    def __init__(self):
        self.contacts = []
        self.load_contacts()

    def load_contacts(self):
        try:
            with open(FILE_NAME, "r", newline="") as f:
                for name, phone, email, address, ctype in csv.reader(f):
                    cls = PersonalContact if ctype == "Personal" else BusinessContact
                    self.contacts.append(cls(name, phone, email, address))
        except FileNotFoundError:
            pass

    def save_contacts(self):
        with open(FILE_NAME, "w", newline="") as f:
            csv.writer(f).writerows(c.to_list() for c in self.contacts)

    # --------- Helper ---------
    def print_contact(self, c, i=None):
        header = f"Contact {i}\n" if i else ""
        print(f"""{header}
Name    : {c.name}
Phone   : {c.phone}
Email   : {c.email}
Address : {c.address}
---------------------------
""")

    # --------- CRUD ---------
    def add_contact(self):
        try:
            data = [
                input("Name: "),
                input("Phone: "),
                input("Email: "),
                input("Address: "),
            ]
            ctype = input("Type (1-Personal, 2-Business): ")
            cls = PersonalContact if ctype == "1" else BusinessContact
            self.contacts.append(cls(*data))
            self.save_contacts()
            print("Contact added successfully!")
        except:
            print("Invalid input.")

    def view_contacts(self):
        if not self.contacts:
            print("No contacts available.")
            return
        for i, c in enumerate(self.contacts, 1):
            self.print_contact(c, i)

    def search_contact(self):
        key = input("Search by name or phone: ").lower()
        found = False
        for c in self.contacts:
            if key in c.name.lower() or key in c.phone:
                self.print_contact(c)
                found = True
        if not found:
            print("Contact not found.")

    def edit_contact(self):
        self.view_contacts()
        try:
            i = int(input("Contact number: ")) - 1
            c = self.contacts[i]
            c.name = input("New Name: ")
            c.phone = input("New Phone: ")
            c.email = input("New Email: ")
            c.address = input("New Address: ")
            self.save_contacts()
            print("Contact updated!")
        except:
            print("Invalid input.")

    def delete_contact(self):
        self.view_contacts()
        try:
            i = int(input("Contact number: ")) - 1
            if input("Are you sure? (y/n): ").lower() == "y":
                self.contacts.pop(i)
                self.save_contacts()
                print("Contact deleted.")
        except:
            print("Invalid input.")

    def export_contacts(self):
        with open("exported_contacts.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Phone", "Email", "Address", "Type"])
            for c in self.contacts:
               writer.writerow(c.to_list())
        print("Contacts exported successfully.")

# ========= Main Menu =========
def main():
    book = AddressBook()
    actions = {
        "1": book.add_contact,
        "2": book.view_contacts,
        "3": book.search_contact,
        "4": book.edit_contact,
        "5": book.delete_contact,
        "6": book.export_contacts
    }

    while True:
        print("\n--- CONTACT BOOK ---")
        print("1.Add  2.View  3.Search  4.Edit  5.Delete  6.Export  7.Exit")
        choice = input("Choose: ")

        if choice == "7":
            print("Goodbye!")
            break
        action = actions.get(choice)
        action() if action else print("Invalid choice.")

if __name__ == "__main__":
    main()