import json
import random
from datetime import datetime, timedelta

# Listor med exempeldata
first_names_male = ["Erik", "Lars", "Karl", "Johan", "Per", "Nils", "Olof", "Anders", "Magnus", "Henrik"]
first_names_female = ["Anna", "Emma", "Elsa", "Sara", "Maria", "Lina", "Sofia", "Eva", "Ida", "Malin"]
last_names = ["Johansson", "Andersson", "Karlsson", "Nilsson", "Eriksson", "Larsson", "Olsson", "Svensson", "Gustafsson", "Pettersson"]
cities = ["Stockholm", "Göteborg"]

# Generera slumpmässigt födelsedatum
def random_birthdate():
    start_date = datetime(1955, 1, 1)
    end_date = datetime(2000, 12, 31)
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

# Generera slumpmässiga personer
def generate_random_employee():
    gender = random.choice(["Male", "Female"])
    if gender == "Male":
        first_name = random.choice(first_names_male)
    else:
        first_name = random.choice(first_names_female)
    
    last_name = random.choice(last_names)
    birthdate = random_birthdate().strftime('%Y-%m-%d')
    city = random.choice(cities)
    salary = random.randint(30000, 70000)
    
    return {
        "first_name": first_name,
        "last_name": last_name,
        "birthdate": birthdate,
        "city": city,
        "salary": salary,
        "gender": gender
    }

# Skapa lista med 20 slumpmässiga anställda
employees = [generate_random_employee() for _ in range(20)]

# Spara som JSON-fil
with open("employees.json", "w") as file:
    json.dump(employees, file, indent=4)

# Visa JSON-datan
print(json.dumps(employees, indent=4))
