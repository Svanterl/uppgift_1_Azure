#Denna koden skulle skickas in i en VM för att visa en matplotlib graf

import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

load_dotenv()

# Databaskonfiguration
server = os.getenv('SQL_SERVER')
database = os.getenv('SQL_DATABASE')
username = os.getenv('SQL_USERNAME')
password = os.getenv('SQL_PASSWORD')
driver = os.getenv('SQL_DRIVER')

# Skapa anslutning till databasen
conn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

# SQL-fråga
query = "SELECT device_id, heart_rate FROM HealthData"

# Hämta data till en pandas DataFrame
df = pd.read_sql(query, conn)

# Gruppera data efter 'device_id' och räkna ut genomsnittlig hjärtfrekvens
df_grouped = df.groupby('device_id').mean()

# Skapa ett stapeldiagram
df_grouped.plot(kind='bar', y='heart_rate', legend=False)
plt.title('Average Heart Rate per Device')
plt.ylabel('Heart Rate')
plt.xlabel('Device ID')

# Visa grafen
plt.show()

# Stäng anslutningen
conn.close()
