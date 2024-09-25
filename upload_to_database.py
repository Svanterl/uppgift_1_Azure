import json
import pyodbc
from azure.storage.queue import QueueServiceClient

# Din Azure Queue Storage Connection String
AZURE_STORAGE_CONNECTION_STRING = 'DefaultEndpointsProtocol=https;AccountName=svante;AccountKey=NsFXHkKpdkCbYh53d5rlHT0MrrjC5/Jp7XVjUpnqhP6THl9Q2nhUI5XikUEIxfg0TvEuuq9jrTi9+AStJjlqjg==;EndpointSuffix=core.windows.net'

# Queue-information
QUEUE_NAME = 'svantequeue'

# Din Azure SQL-databasuppgifter
server = 'svantede23.database.windows.net'
database = 'svantede23'
username = 'CloudSA9c3d845b'
password = 'Svante1996'
driver = '{ODBC Driver 17 for SQL Server}'  # Kontrollera att du har rätt ODBC-drivrutin installerad

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
