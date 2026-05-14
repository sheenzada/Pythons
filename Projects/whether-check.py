import requests

def get_weather(city_name, api_key):
    # Base URL for the OpenWeatherMap API
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    # Complete URL with parameters
    # units=metric gives Celsius, units=imperial gives Fahrenheit
    complete_url = f"{base_url}q={city_name}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(complete_url)
        data = response.json()
        
        if data["cod"] != "404":
            main = data["main"]
            weather = data["weather"][0]
            
            temp = main["temp"]
            pressure = main["pressure"]
            humidity = main["humidity"]
            description = weather["description"]
            
            print(f"--- Weather in {city_name.upper()} ---")
            print(f"Temperature: {temp}°C")
            print(f"Humidity:    {humidity}%")
            print(f"Condition:   {description.capitalize()}")
        else:
            print("City Not Found!")
            
    except Exception as e:
        print(f"An error occurred: {e}")

# --- CONFIGURATION ---
MY_API_KEY = "your_api_key_here"  # Replace with your actual API key
city = input("Enter city name: ")

get_weather(city, MY_API_KEY)