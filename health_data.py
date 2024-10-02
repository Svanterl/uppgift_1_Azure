#Koden som genererar JSON filen

import json
import random
import datetime

def generate_health_data(device_id, timestamp):
    data = {
        "device_id": device_id,  # Device ID som ökar från 1 till 50
        "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3],  # Tidsstämpel med millisekunder
        "heart_rate": random.randint(60, 100),  # Puls (slag/minut)
        "blood_pressure": {
            "systolic": random.randint(110, 140),  # Systoliskt blodtryck (mmHg)
            "diastolic": random.randint(70, 90)  # Diastoliskt blodtryck (mmHg)
        },
        "spo2": random.randint(90, 100),  # Syremättnad i blodet (%)
        "steps_taken": random.randint(0, 10000)  # Antal steg tagna under dagen
    }
    return data

health_data_list = []

for device_id in range(1, 51):
    timestamp = datetime.datetime.now() - datetime.timedelta(minutes=device_id)
    health_data = generate_health_data(device_id, timestamp)
    health_data_list.append(health_data)

with open('health_data.json', 'w') as json_file:
    json.dump(health_data_list, json_file, indent=4)

print("50 rader av hälsovårdsdata har genererats med device_id från 1 till 50 och sparats i 'health_data.json'.")
