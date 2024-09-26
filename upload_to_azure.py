from azure.storage.queue import QueueServiceClient
import os
from dotenv import load_dotenv

# Ladda miljövariabler från .env-filen
load_dotenv()

# Hämta Azure Storage Connection String och Queue Name från .env
AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
QUEUE_NAME = os.getenv('QUEUE_NAME')
LOCAL_FILE_NAME = os.getenv('LOCAL_FILE_NAME', 'employees.json')  # Sätter ett standardvärde om variabeln inte finns i .env

def send_to_azure_queue():
    try:
        # Anslut till QueueServiceClient med din connection string
        queue_service_client = QueueServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

        # Hämta en QueueClient för den angivna kön
        queue_client = queue_service_client.get_queue_client(QUEUE_NAME)

        # Läs innehållet i filen och skicka som ett meddelande till kön
        with open(LOCAL_FILE_NAME, "r") as file:
            file_content = file.read()
            queue_client.send_message(file_content)
        
        print(f"Innehållet i filen '{LOCAL_FILE_NAME}' har skickats till Azure Queue '{QUEUE_NAME}'.")

    except Exception as e:
        print(f"Det uppstod ett fel: {str(e)}")

if __name__ == "__main__":
    # Kontrollera om filen finns innan uppladdning
    if os.path.exists(LOCAL_FILE_NAME):
        send_to_azure_queue()
    else:
        print(f"Filen '{LOCAL_FILE_NAME}' hittades inte.")
