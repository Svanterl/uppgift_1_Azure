#Denna koden skickar JSON filen till min queue

from azure.storage.queue import QueueServiceClient
import os
from dotenv import load_dotenv
import json

load_dotenv()

AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
QUEUE_NAME = os.getenv('QUEUE_NAME')
LOCAL_FILE_NAME = os.getenv('LOCAL_FILE_NAME', 'health_data.json')

def send_to_azure_queue():
    try:
        queue_service_client = QueueServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

        queue_client = queue_service_client.get_queue_client(QUEUE_NAME)

        with open(LOCAL_FILE_NAME, "r") as file:
            health_data = json.load(file)

            health_data_json = json.dumps(health_data)

            queue_client.send_message(health_data_json)

        print(f"Innehållet i filen '{LOCAL_FILE_NAME}' har skickats som ett meddelande till Azure Queue '{QUEUE_NAME}'.")

    except Exception as e:
        print(f"Det uppstod ett fel: {str(e)}")

if __name__ == "__main__":
    if os.path.exists(LOCAL_FILE_NAME):
        send_to_azure_queue()
    else:
        print(f"Filen '{LOCAL_FILE_NAME}' hittades inte.")
