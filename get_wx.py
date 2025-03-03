import requests  # Import the requests library to make HTTP requests to the weather API

# Function to get weather data from the API
def get_weather(city):
    # Define the base URL for WeatherAPI
    base_url = "http://api.weatherapi.com/v1/current.json"  # Endpoint for current weather data
    api_key = "3c79a71e5c9e4a4cbed172211250303"  # Replace with your API key from WeatherAPI
    
    # Set the parameters for the API request
    params = {
        "key": api_key,  # API key for authentication
        "q": city,  # City name entered by the user
        "aqi": "no"  # Optional parameter to disable air quality info (we’re not using it here)
    }

    try:
        # Send a GET request to WeatherAPI with the specified parameters
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an error if the response code is not 200 (OK)
        return response.json()  # Return the JSON data from the API response
    except requests.exceptions.RequestException as e:  # Catch any errors that occur during the request
        print(f"Error fetching weather data: {e}")  # Print the error message if something goes wrong
        return None  # Return None if there's an error

# Function to display the weather data in a human-readable format
def display_weather(weather_data):
    if weather_data:  # Check if weather data is available (i.e., not None)
        # Extract specific data from the response
        location = weather_data["location"]  # Get the location data
        current = weather_data["current"]  # Get the current weather data
        
        # Extract relevant details for display
        city_name = location["name"]  # City name
        region = location["region"]  # Region (state/province)
        country = location["country"]  # Country name
        temperature = current["temp_c"]  # Current temperature in Celsius
        humidity = current["humidity"]  # Current humidity percentage
        description = current["condition"]["text"]  # Weather description (e.g., "Clear", "Rainy")
        wind_speed = current["wind_kph"]  # Wind speed in kilometers per hour
        
        # Print the weather details in a readable format
        print(f"\nWeather in {city_name}, {region}, {country}:")
        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")
        print(f"Description: {description}")
        print(f"Wind Speed: {wind_speed} kph\n")
    else:
        print("Unable to display weather data.")  # If no data, print an error message

# Main function to run the application
def main():
    city = input("Enter city name: ").strip()  # Prompt the user to enter a city name
    weather_data = get_weather(city)  # Call the get_weather function to fetch data
    display_weather(weather_data)  # Call the display_weather function to show the results

# Ensure the script runs when executed directly (not imported as a module)
if __name__ == "__main__":
    main()  # Call the main function to start the app
