import csv

EMAIL_TEMPLATE = """Hi {name},

My name is Rohith Athrey and I'm a freshman at the University of Maryland studying Computer Science. I came across your LinkedIn profile while searching for UMD alumni at {company}.

I have a strong interest in Software Engineering and would love to speak with you to learn more about your career and path. Would you be willing to arrange a quick, 10-15 minute phone call at your earliest convenience?

My resume is attached for your consideration. Thank you, and I look forward to connecting with you soon.

Best,
Rohith Athrey"""

EMAIL_SUBJECT = "UMD Student reaching out"

def read_contacts(filename):
    contacts = []
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Strip whitespace from values
                contact = {
                    'email': row['email'].strip(),
                    'name': row['name'].strip(),
                    'company': row['company'].strip()
                }
                contacts.append(contact)
        return contacts
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

def personalize_email(template, contact):
    """Personalize email template with contact information"""
    try:
        personalized_message = template.format(
            name=contact['name'],
            company=contact['company']
        )
        return personalized_message
    except KeyError as e:
        print(f"Error: Missing field {e} in contact data")
        return None
    except Exception as e:
        print(f"Error personalizing email: {e}")
        return None

def validate_contact(contact):
    """Validate that contact has required fields"""
    required_fields = ['email', 'name', 'company']
    for field in required_fields:
        if field not in contact or not contact[field]:
            return False
    return True

if __name__ == "__main__":
    contacts = read_contacts('contacts.csv')
    if contacts:
        print(f"\nRead {len(contacts)} contacts from CSV:")
        for contact in contacts:
            if validate_contact(contact):
                personalized = personalize_email(EMAIL_TEMPLATE, contact)
                if personalized:
                    print(f"\nEmail to {contact['email']}:")
                    print(f"Subject: {EMAIL_SUBJECT}")
                    print(personalized)
                    print("-" * 50)
            else:
                print(f"Invalid contact data: {contact}")   
    else:
        print("No contacts found or error reading file.")