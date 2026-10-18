import requests
import pandas as pd

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