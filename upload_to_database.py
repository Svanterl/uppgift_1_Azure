import os
import json
import pyodbc
from azure.storage.queue import QueueServiceClient
from dotenv import load_dotenv

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
            employees = json.loads(message_content)

            # Radera meddelandet från kön efter bearbetning
            queue_client.delete_message(queue_message.id, queue_message.pop_receipt)

            return employees
        else:
            print("Inga meddelanden i kön.")
            return None

    except Exception as e:
        print(f"Det uppstod ett fel vid mottagandet från kön: {str(e)}")
        return None

def insert_into_sql(employees):
    try:
        # Anslut till SQL-servern
        conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
        cursor = conn.cursor()

        # Loopa genom varje anställd och infoga i databasen
        for employee in employees:
            cursor.execute('''
                INSERT INTO Employees (first_name, last_name, birthdate, city, salary, gender)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', employee['first_name'], employee['last_name'], employee['birthdate'], employee['city'], employee['salary'], employee['gender'])
        
        # Spara ändringarna
        conn.commit()
        print("Alla anställda har laddats upp till databasen.")

    except Exception as e:
        print(f"Det uppstod ett fel vid SQL-uppdateringen: {str(e)}")
    
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    employees = receive_from_queue()
    if employees:
        insert_into_sql(employees)
