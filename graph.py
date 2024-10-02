#Koden som finns i min VM som visar grafen

import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
import matplotlib

matplotlib.use('Agg')

load_dotenv()

server = os.getenv('SQL_SERVER')
database = os.getenv('SQL_DATABASE')
username = os.getenv('SQL_USERNAME')
password = os.getenv('SQL_PASSWORD')
driver = os.getenv('SQL_DRIVER')

connection_string = f"mssql+pyodbc://{username}:{password}@{server}:1433/{database}?driver={driver}"
engine = create_engine(connection_string)

try:
    query = "SELECT device_id, heart_rate FROM HealthData"

    df = pd.read_sql(query, engine)

    print("Data hämtad:")
    print(df)

    df_grouped = df.groupby('device_id').mean()

    df_grouped.plot(kind='bar', y='heart_rate', legend=False)
    plt.title('Average Heart Rate per Device')
    plt.ylabel('Heart Rate')
    plt.xlabel('Device ID')

    plt.savefig('average_heart_rate.png')

    print("Grafen har sparats som 'average_heart_rate.png'.")

except Exception as e:
    print(f"Ett fel inträffade: {e}")

finally:
    engine.dispose()
