import requests
from dotenv import load_dotenv
load_dotenv()

def sum(a,b):
    return a+b

def calculate_discount(price: float, discount: float) -> dict:
    final_price = price - (price * discount / 100)
    return {
        "original_price": price,
        "discount": discount,
        "final_price": round(final_price, 2)
    }

def get_weather(city: str) -> str:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = ("https://api.openweathermap.org/data/2.5/weather"f"?q={city}&appid={api_key}&units=metric")
    
    # using requests   openweathermap URL 
    response = requests.get(url)
    if response.status_code != 200:
        return "Weather lookup failed"
    data=response.json()
    return (f"{city}: "f"{data['weather'][0]['description']}, "f"{data['main']['temp']}°C")

#print(sum(1000,10))

#print(calculate_discount(1000,10))

#print(get_weather("boston"))