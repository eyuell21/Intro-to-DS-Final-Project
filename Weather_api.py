
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_KEY = "d0c52a54f450bc7a4d46b600bdd12061"
CITY_NAME = "Tokyo"

url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={API_KEY}&units=metric"

response = requests.get(url)
print(response)
data = response.json()

print(data)

if "main" in data:
    city = data["name"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    weather = data["weather"][0]["description"]

    print(f"City: {city}\nTemperature: {temp}°C\nHumidity: {humidity}%\nWeather: {weather}")
else:
    print("Error fetching weather data.")

data_dict = {
    "City": [city],
    "Temperature (°C)": [temp],
    "Humidity (%)": [humidity],
    "Weather Description": [weather]
}

weather_df = pd.DataFrame(data_dict)
print(weather_df)

weather_df.to_csv("weather_data.csv", index=False)
print("Data saved to weather_data.csv")

plt.figure(figsize=(6,4))
plt.bar(weather_df["City"], weather_df["Temperature (°C)"], color='skyblue')
plt.xlabel("City")
plt.ylabel("Temperature (°C)")
plt.title("Current Temperature")
plt.show()


cities = ["London", "New York", "Paris", "Tokyo", "Sydney"]
weather_data = []

for city in cities:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if "main" in data:
        weather_data.append({
            "City": city,
            "Temperature (°C)": data["main"]["temp"],
            "Humidity (%)": data["main"]["humidity"],
            "Weather Description": data["weather"][0]["description"]
        })

# Convert to DataFrame
multi_city_df = pd.DataFrame(weather_data)
print(multi_city_df)

plt.figure(figsize=(8,5))
plt.bar(multi_city_df["City"], multi_city_df["Temperature (°C)"], color='coral')
plt.xlabel("City")
plt.ylabel("Temperature (°C)")
plt.title("Weather Comparison Across Cities")
plt.show()