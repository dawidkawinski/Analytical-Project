import requests
import pandas as pd
import os 
from google.cloud import bigquery

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 51.25, 
    "longitude": 22.57,
    "hourly": ["temperature_2m", "precipitation"],
    "timezone": "Europe/Warsaw"
}

response = requests.get(url, params=params)
data = response.json()

df = pd.DataFrame({
    "datetime": data["hourly"]["time"],
    "temperature": data["hourly"]["temperature_2m"],
    "precipitation": data["hourly"]["precipitation"]
})

print(df.head())

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp-key.json"

client = bigquery.Client()

table_id = "splendid-watch-512007-p6.weather_data.lublin_forecast"

print("Wysyłanie danych do BigQuery...")

job_config = bigquery.LoadJobConfig(
    write_disposition="WRITE_APPEND",
)

job = client.load_table_from_dataframe(
    df, table_id, job_config=job_config
)

job.result()

print(f"Sukces! Załadowano {job.output_rows} wierszy do tabeli {table_id}.")