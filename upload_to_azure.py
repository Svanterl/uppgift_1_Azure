from azure.storage.queue import QueueServiceClient
import os

# Din Azure Storage Connection String
AZURE_STORAGE_CONNECTION_STRING = 'DefaultEndpointsProtocol=https;AccountName=svante;AccountKey=NsFXHkKpdkCbYh53d5rlHT0MrrjC5/Jp7XVjUpnqhP6THl9Q2nhUI5XikUEIxfg0TvEuuq9jrTi9+AStJjlqjg==;EndpointSuffix=core.windows.net'

# Namn på den queue där du vill skicka meddelandet
QUEUE_NAME = 'svantequeue'

# Namnet på filen som du vill läsa och skicka som ett meddelande
LOCAL_FILE_NAME = 'employees.json'

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
