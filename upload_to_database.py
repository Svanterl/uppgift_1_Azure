#Detta är koden som skickar data mellan queue och databasen.

import os
import json
import pyodbc
from azure.storage.queue import QueueServiceClient
from dotenv import load_dotenv
from datetime import datetime

# Ladda in miljövariabler från .env-filen
load_dotenv()

# Din Azure Queue Storage Connection String och andra variabler från .env
AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
QUEUE_NAME = os.getenv('QUEUE_NAME')

# Din Azure SQL-databasuppgifter
server = os.getenv('SQL_SERVER')
database = os.getenv('SQL_DATABASE')
username = os.getenv('SQL_USERNAME')
password = os.getenv('SQL_PASSWORD')
driver = os.getenv('SQL_DRIVER')

def receive_from_queue():
    try:
        # Anslut till QueueServiceClient
        queue_service_client = QueueServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        queue_client = queue_service_client.get_queue_client(QUEUE_NAME)

        # Hämta ett meddelande från kön
        queue_message = queue_client.receive_message()

        if queue_message:
            # Extrahera meddelandetexten
            message_content = queue_message.content
            health_data = json.loads(message_content)

            # Radera meddelandet från kön efter bearbetning
            queue_client.delete_message(queue_message.id, queue_message.pop_receipt)

            return health_data
        else:
            print("Inga meddelanden i kön.")
            return None

    except Exception as e:
        print(f"Det uppstod ett fel vid mottagandet från kön: {str(e)}")
        return None

def insert_into_sql(health_data):
    try:
        # Anslut till SQL-servern
        conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
        cursor = conn.cursor()

        # Loopa genom varje hälsodata och kontrollera dubbletter
        for entry in health_data:
            # Kontrollera om datan redan finns i databasen baserat på device_id och timestamp
            cursor.execute('''
                SELECT COUNT(*)
                FROM HealthData
                WHERE device_id = ? AND timestamp = ?
            ''', entry['device_id'], entry['timestamp'])
            exists = cursor.fetchone()[0]  # Hämta antalet dubbletter

            # Konvertera timestamp till datetime-objekt
            try:
                timestamp = datetime.fromisoformat(entry['timestamp'])  # Konvertera till datetime-objekt
            except ValueError:
                print(f"Ogiltigt tidsstämpelformat för device_id {entry['device_id']}: {entry['timestamp']}")
                continue  # Hoppa över detta meddelande

            if exists == 0:
                # Om det inte finns, infoga i databasen
                cursor.execute('''INSERT INTO HealthData (device_id, timestamp, heart_rate, systolic, diastolic, spo2, steps_taken)
                                  VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                               entry['device_id'], timestamp, entry['heart_rate'], 
                               entry['blood_pressure']['systolic'], entry['blood_pressure']['diastolic'], 
                               entry['spo2'], entry['steps_taken'])
                print(f"Data för device_id {entry['device_id']} vid {timestamp} har lagts till i databasen.")
            else:
                print(f"Data för device_id {entry['device_id']} vid {timestamp} finns redan i databasen.")

        # Spara ändringarna
        conn.commit()
        print("Alla nya hälsodata har laddats upp till databasen.")

    except Exception as e:
        print(f"Det uppstod ett fel vid SQL-uppdateringen: {str(e)}")
    
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    health_data = receive_from_queue()
    if health_data:
        insert_into_sql(health_data)
