import csv
#file name;all contacts get saved/ loaded
_file = "address book.csv"

#Parent(super) class
class Contact: 
    """base class. Stores fields to all contacts. """     
    def __init__(self, name, phone, email, address):
        """used to initialize the parameters"""
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
    def summary(self):
        """
        return human readable summary of contacts.
        used when printing to the terminal
        """
        return f"{self.name} | {self.phone} | {self.email} | {self.address}"
    def matching_names(self, inquery):
        """ to avoide case sensitivety"""
        return inquery.lower() in self.name.lower()
    def matching_phone(self, inquery):
        """checks if inquery is inside phone"""
        return inquery in self.phone
    def to_csv(self):
        """ returns list for csv export"""
        return [self.name, self.phone, self.email, self.address]
    
 #Child class1
class PersonalConact(Contact):   
    """to store Personal contacts"""
    def __init__ (self, name, phone, email, address):
        super().__init__ (name, phone, email, address)
    def summary(self):
        """Override summary to show contact type in the terminal."""
        base = super().summary()
        return "[Personal]" + base
    
#Child class2
class BusinessContact(Contact): 
    """ to store business contacts"""
    def __init__(self, name, phone, email, address, company=None, job_title=None):
        super().__init__ (name, phone, email, address)
        self.company = company
        self.job_title = job_title
    def summary(self):
        """Override summary to show contact type and optional company/job."""
        base = super().summary()
        extra = ""
        if self.company:
            extra += f" | {self.company}"
        if self.job_title:
            extra += f" - {self.job_title}"
        return "[Business]" + base + extra


#Manager class
class AddressBook:
    """soters and manages contact"""
    
    #managing
    def __init__(self):
        #list of contct
        self.contacts = []
    # adding, listing, searching
    def add_contact(self, contact):
        """Add new contact object"""
        self.contacts.append(contact)
    def list_contacts(self):
        """print all contacts"""
        if not self.contacts:
            print("\nNo contacts yet.")
            return
        print("\n=== CONTACT LIST ===")
        for i, c in enumerate(self.contacts, start=1):
            #enumerate is an function to return two lists; i=numbers, c=contact
            print(f'{i}. {c.summary()}')
    def search_by_name(self, inquery):
        """print all conatacts names that match the inquery"""
        print(f"\nSearching for name containing: '{inquery}'")
        results = [c for c in self.contacts if c.matching_names(inquery)]
        if not results:
            print('No contacts found with this name')
        else:
            for c in results:
                print("-", c.summary())
    def search_by_phone(self, inquery):
        """print all conatacts whose phone number match the inquery"""
        print(f"\nSearching for phone containing: '{inquery}'")
        results = [c for c in self.contacts if c.matching_phone(inquery)]
        if not results:
            print('No contacts found with this phone number')
        else:
            for c in results:
                print("-", c.summary())
    
    #editing and deleting
    def delete_contact(self, index):
        """delete contacts by 1 based index"""
        if index < 1 or index > len(self.contacts):
            print('invalid index')
            return
        removed = self.contacts.pop(index - 1)
        print(f'Deleted: {removed.summary()}')
    def edit_contact(self, index):
        """
        edit an existing contact chosen by 1 based index.
        Enter to keep old value.
        """
        if index < 1 or index > len(self.contacts):
            print('invalid index')
            return
        contact = self.contacts[index - 1]
        print('\n editing contact: ')
        print(contact.summary())
        print('Press Enter to keep the current value')
        
        #Asking for new values
        new_name = input(f'Enter new name [{contact.name}]: ').strip()
        new_phone = input(f'Enter new phone number [{contact.phone}]: ').strip()
        new_email = input(f'Enter new email [{contact.email}]: ').strip()
        new_address = input(f'Enter new address [{contact.address}]: ').strip()
        #only change if user entered something
        if new_name:
            contact.name = new_name
        if new_phone:
            contact.phone = new_phone
        if new_email:
            contact.email = new_email
        if new_address:
            contact.address = new_address
        print('Contact updated:')
        print(contact.summary())
        
        #File I/O
    def load_from_csv(self, filename):
        """
       Load contacts from a CSV file.
       Type, Name, Phone, Email, Address
       where Type is: "personal", "business", or something else.
       """
        try:
            with open(filename, "r", newline="", encoding="utf-8") as f:       # utf-8 Allows names with any language characters
                reader = csv.reader(f)
                rows = list(reader)
                if not rows:
                    return
            for row in rows:
                #  We expect EXACTLY 5 values
                if len(row) < 5:
                    continue    #skip
                ctype = row[0].strip().lower()
                name = row[1].strip()
                phone = row[2].strip()
                email = row[3].strip()
                address = row[4].strip()
                        
                if ctype == "personal":
                    contact = PersonalConact(name, phone, email, address)
                elif ctype == "business":
                    contact = BusinessContact(name, phone, email, address)
                else:       #  if type not recognized treat like normal Contact
                    contact = Contact(name, phone, email, address)
                            
                self.contacts.append(contact)
        except FileNotFoundError:
            print('Error loading from file')
                
                
    def export_to_csv(self, filename):
        """save all contacts to a csv file"""
        try:
            with open(filename, mode="w", newline="", encoding= "utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Type", "Name", "Phone", "Email", "Address"])
                for c in self.contacts:
                    if isinstance(c, PersonalConact):
                        #isinstance checks whether an object belongs to a specific class.
                        ctype = "personal"
                    elif isinstance(c, BusinessContact):
                        ctype = "business"
                    else:
                        ctype = "contact"
                    writer.writerow([ctype] + c.to_csv())
                    #c.to_csv() returns [name, phone, email, address]
            print(f"\nContact exported to '{filename}'.")
        except Exception as e:
            print(f'Error exporting to file: {e}')


#user interface(interaction with user)
def add_personal_contact_ui(book):
    """
    Ask the user for personal contact details,
    create a PersonalContact and add it to the address book
    """
    print("\n=== ADD PERSONAL CONTACT===")
    name = input("Name: ").strip()
    phone = input('Phone number: ').strip()
    email = input('Email: ').strip()
    address = input('Address: ').strip()
    
    if not name or not phone:
        print('Name and phone number required')
        return
    contact = PersonalConact(name, phone, email, address)
    book.add_contact(contact)
    print('Personal contact added')
    
def add_business_contact_ui(book):
    """
    Ask the user for business contact details,
    create a BusinessContact and add it to the address book.
    """
    print('\n=== ADD BUSINESS CONTACT ===')
    name = input('Name: ').strip()
    phone = input('Phone number: ').strip()
    email = input('Email: ').strip()
    address = input('Address: ').strip()
    company = input('Company (optional): ').strip()
    job_title = input('Job title: ').strip()
    
    if not name or not phone:
        print('Name and Phone number are required')
        return
    contact = BusinessContact(name, phone, email, address, company or None, job_title or None)
    book.add_contact(contact)
    print('business contact added')
    
def choose_contact_index(book, action_name="select"):
    """
   Ask the user to choose a contact by number.
   - Shows the contact list.
   - Returns a 1-based index (int) if valid.
   - Returns None if user cancels or input is invalid.
   """
    #if no contact cant select
    if not book.contacts:
        print('No contacts to choose from')
        return None
    
    #show currennt list
    book.list_contacts()
    try:
        #ask:which contact?
        raw = input(f"\nEnter the contact number to{action_name} (or press Enter to cancel): ").strip()
        #empty input = user cancled
        if raw == "":
            return None
        index = int(raw)
        #check if index is in valid range
        if 1 <= index <= len(book.contacts):
            return index
        else:
            print(f'please enter 1 - {len(book.contacts)}.')
            return None
    except ValueError:
        print('Invalid number.')
        return None
        
def main_manu():
    """
   Main loop for the address book program.
   - Creates an AddressBook instance.
   - Loads contacts from a CSV file.
   - Repeatedly shows a menu and performs the selected action.
   - Exports contacts and exits when the user chooses option 8.
   """
    book = AddressBook()
    book.load_from_csv(_file)
    
    # main loop
    while True:
        print('\n===== ADDRESS BOOK MENU =====')
        print('1.Add Personal Contact')
        print('2.Add Business Contact')
        print('3.List All Contacts')
        print('4.Search by Name')
        print('5. Search by Phone')
        print('6.Edit Contact')
        print('7.Delete Contact')
        print('8.Export & Exit')
        
        choice = input('choose an option (1-8): ').strip()
        if choice == '1':
            add_personal_contact_ui(book)
        elif choice == '2':
            add_business_contact_ui(book)
        elif choice == '3':
            book.list_contacts()
        elif choice == '4':
            q = input('Enter name or part of it: ').strip()
            if q:
                book.search_by_name(q)
            else:
                print('Empty search')
        elif choice == '5':
            q = input('Enter phone number or part of it: ').strip()
            if q:
                book.search_by_phone(q)
            else:
                print('Empty search')
        elif choice == '6':
            idx = choose_contact_index(book, "edit")
            if idx is not None:
                book.edit_contact(idx)
        elif choice == '7':
            idx = choose_contact_index(book, "delete")
            if idx is not None:
                book.delete_contact(idx)
        elif choice == '8':
            book.export_to_csv(_file)
            print('Goodbye')
            break
        else:
            print('Invalid choice, please enter a number from 1 to 8')
if __name__ == "__main__":
    main_manu()