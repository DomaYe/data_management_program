from faker import Faker
import random
import pandas as pd

fake = Faker()

# Defining the three entities: Person, Pet, Occupation
class Person:
    def __init__(self, person_id, full_name, address):
        self.person_id = person_id
        self.full_name = full_name
        self.address = address

    def to_dict(self):
        return {
            "person_id": self.person_id,
            "full_name": self.full_name,
            "address": self.address
        }

    @staticmethod
    def from_dict(data):
        return Person(
            person_id=int(data["person_id"]),
            full_name=data["full_name"],
            address=data["address"]
        )

class Pet:
    def __init__(self, pet_id, owner_id, pet_name, species):
        self.pet_id = pet_id
        self.owner_id = owner_id
        self.pet_name = pet_name
        self.species = species

    def to_dict(self):
        return {
            "pet_id": self.pet_id,
            "owner_id": self.owner_id,
            "pet_name": self.pet_name,
            "species": self.species
        }

    @staticmethod
    def from_dict(data):
        return Pet(
            pet_id=data["pet_id"],
            owner_id=int(data["owner_id"]),
            pet_name=data["pet_name"],
            species=data["species"]
        )

class Occupation:
    def __init__(self, occupation_id, person_id, occupation, company):
        self.occupation_id = occupation_id
        self.person_id = person_id
        self.occupation = occupation
        self.company = company

    def to_dict(self):
        return {
            "occupation_id": self.occupation_id,
            "person_id": self.person_id,
            "occupation": self.occupation,
            "company": self.company
        }

    @staticmethod
    def from_dict(data):
        return Occupation(
            occupation_id=data["occupation_id"],
            person_id=int(data["person_id"]),
            occupation=data["occupation"],
            company=data["company"]
        )

# Data generator function with Faker
def generate_data(num_records):
    persons = []
    pets = []
    occupations = []

    for i in range(num_records):
        # Generate persons
        person = Person(person_id=i, full_name=fake.name(), address=fake.address())
        persons.append(person)

        # Generate pets related to the person (1:N relationship)
        num_pets = random.randint(1, 3)
        for j in range(num_pets):
            pet = Pet(
                pet_id=f"{i}_{j}",
                owner_id=i,
                pet_name=fake.first_name(),
                species=random.choice(['Dog', 'Cat', 'Bird', 'Rabbit'])
            )
            pets.append(pet)

        # Generate occupations related to the person (1:N relationship)
        num_occupations = random.randint(1, 2)
        for k in range(num_occupations):
            occupation = Occupation(
                occupation_id=f"{i}_{k}",
                person_id=i,
                occupation=fake.job(),
                company=fake.company()
            )
            occupations.append(occupation)

    return persons, pets, occupations

# Export to CSV
def export_to_csv(persons, pets, occupations):
    df_persons = pd.DataFrame([p.to_dict() for p in persons])
    df_persons.to_csv('persons.csv', index=False, encoding='utf-8')

    df_pets = pd.DataFrame([p.to_dict() for p in pets])
    df_pets.to_csv('pets.csv', index=False, encoding='utf-8')

    df_occupations = pd.DataFrame([o.to_dict() for o in occupations])
    df_occupations.to_csv('occupations.csv', index=False, encoding='utf-8')

# Import from CSV
def import_from_csv():
    df_persons = pd.read_csv('persons.csv', encoding='utf-8')
    persons = [Person.from_dict(row.to_dict()) for _, row in df_persons.iterrows()]

    df_pets = pd.read_csv('pets.csv', encoding='utf-8')
    pets = [Pet.from_dict(row.to_dict()) for _, row in df_pets.iterrows()]

    df_occupations = pd.read_csv('occupations.csv', encoding='utf-8')
    occupations = [Occupation.from_dict(row.to_dict()) for _, row in df_occupations.iterrows()]

    return persons, pets, occupations

# Export to JSON
def export_to_json(persons, pets, occupations):
    df_persons = pd.DataFrame([p.to_dict() for p in persons])
    df_persons.to_json('persons.json', orient='records', indent=4, force_ascii=False)

    df_pets = pd.DataFrame([p.to_dict() for p in pets])
    df_pets.to_json('pets.json', orient='records', indent=4, force_ascii=False)

    df_occupations = pd.DataFrame([o.to_dict() for o in occupations])
    df_occupations.to_json('occupations.json', orient='records', indent=4, force_ascii=False)

# Import from JSON
def import_from_json():
    df_persons = pd.read_json('persons.json', encoding='utf-8')
    persons = [Person.from_dict(row.to_dict()) for _, row in df_persons.iterrows()]

    df_pets = pd.read_json('pets.json', encoding='utf-8')
    pets = [Pet.from_dict(row.to_dict()) for _, row in df_pets.iterrows()]

    df_occupations = pd.read_json('occupations.json', encoding='utf-8')
    occupations = [Occupation.from_dict(row.to_dict()) for _, row in df_occupations.iterrows()]

    return persons, pets, occupations

# Export to XLSX
def export_to_xlsx(persons, pets, occupations):
    with pd.ExcelWriter('dataset.xlsx') as writer:
        pd.DataFrame([p.to_dict() for p in persons]).to_excel(writer, sheet_name='Persons', index=False)
        pd.DataFrame([p.to_dict() for p in pets]).to_excel(writer, sheet_name='Pets', index=False)
        pd.DataFrame([o.to_dict() for o in occupations]).to_excel(writer, sheet_name='Occupations', index=False)

# Import from XLSX
def import_from_xlsx():
    xls = pd.ExcelFile('dataset.xlsx')
    df_persons = pd.read_excel(xls, 'Persons')
    persons = [Person.from_dict(row.to_dict()) for _, row in df_persons.iterrows()]

    df_pets = pd.read_excel(xls, 'Pets')
    pets = [Pet.from_dict(row.to_dict()) for _, row in df_pets.iterrows()]

    df_occupations = pd.read_excel(xls, 'Occupations')
    occupations = [Occupation.from_dict(row.to_dict()) for _, row in df_occupations.iterrows()]

    return persons, pets, occupations

# Generating sample data and exporting
if __name__ == "__main__":
    persons, pets, occupations = generate_data(10)
    export_to_csv(persons, pets, occupations)
    export_to_json(persons, pets, occupations)
    export_to_xlsx(persons, pets, occupations)
