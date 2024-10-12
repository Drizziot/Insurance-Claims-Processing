import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from datetime import datetime
import sys

# List of outdoor activities with their optimal temperature ranges in Fahrenheit
ACTIVITIES = [
    {"name": "Hiking", "temp_min": 50, "temp_max": 70},  # Temp range in Fahrenheit
    # Add more activities as needed
]

def get_location():
    """Retrieves the user's location based on their IP address."""
    try:
        response = requests.get("http://ip-api.com/json/")
        data = response.json()
        if data['status'] == 'success':
            return {
                'city': data['city'],
                'lat': data['lat'],
                'lon': data['lon']
            }
        else:
            messagebox.showerror("Error", "Unable to retrieve location.")
            return None
    except Exception as e:
        messagebox.showerror("Error", f"Error retrieving location: {e}")
        return None

def fetch_weather(lat, lon, api_key):
    """Fetches the 5-day weather forecast from OpenWeatherMap in Fahrenheit."""
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=imperial&appid={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if data['cod'] != '200':
            messagebox.showerror("Error", f"Error fetching weather data: {data.get('message', 'Unknown error')}")
            return None
        return data
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching weather data: {e}")
        return None

def fetch_headlines():
    """Fetches top global news headlines."""
    NEWS_API_KEY = 'd25e4bd16a2f43dc9fda31b3919bef53'
    url = f"https://newsapi.org/v2/top-headlines?language=en&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if data['status'] != 'ok':
            messagebox.showerror("Error", f"Error fetching news data: {data.get('message', 'Unknown error')}")
            return None
        return data['articles']
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching news data: {e}")
        return None

def analyze_weather(data, preferences):
    """Analyzes the weather data against user preferences and activity optimal temperatures."""
    optimal_times = []
    for entry in data['list']:
        temp = entry['main']['temp']  # Temp is now in Fahrenheit
        humidity = entry['main']['humidity']
        condition = entry['weather'][0]['main']
        if (preferences['temp_min'] <= temp <= preferences['temp_max'] and
                preferences['humidity_min'] <= humidity <= preferences['humidity_max'] and
                condition in preferences['conditions']):
            time = datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d %H:%M')
            suitable_activities = [activity['name'] for activity in ACTIVITIES if activity['temp_min'] <= temp <= activity['temp_max']]
            optimal_times.append({
                'datetime': time,
                'temp': temp,
                'humidity': humidity,
                'condition': condition,
                'activities': suitable_activities
            })
    return optimal_times

class WeatherPreferenceGUI:
    def __init__(self, master):
        self.master = master
        master.title("Weather and Top Headlines")
        master.geometry("700x600")
        master.configure(bg="white")  # Set the background color to azure
        
        self.location = get_location()
        if not self.location:
            sys.exit(1)

        self.create_widgets()

    def create_widgets(self):
        # Set the background of labels, text areas, and frames to azure
        ttk.Label(self.master, text=f"Detected Location: {self.location['city']}", font=('times new roman', 14), background="white").pack(pady=10)

        # Temperature range setup in Fahrenheit
        ttk.Label(self.master, text="Temperature Range (°F):", background="white").pack()
        self.temp_min = tk.IntVar()
        self.temp_max = tk.IntVar()
        ttk.Entry(self.master, textvariable=self.temp_min).pack()
        ttk.Entry(self.master, textvariable=self.temp_max).pack()

        # Humidity range setup
        ttk.Label(self.master, text="Humidity Range (%):", background="white").pack()
        self.humidity_min = tk.IntVar()
        self.humidity_max = tk.IntVar()
        ttk.Entry(self.master, textvariable=self.humidity_min).pack()
        ttk.Entry(self.master, textvariable=self.humidity_max).pack()

        # Weather conditions setup
        ttk.Label(self.master, text="Select Weather Conditions:", background="white").pack()
        self.condition_vars = {}
        for condition in ["Clear", "Clouds", "Rain", "Snow"]:
            var = tk.BooleanVar()
            ttk.Checkbutton(self.master, text=condition, variable=var).pack()
            self.condition_vars[condition] = var

        # Submit button
        ttk.Button(self.master, text="Find Optimal Times and Activities", command=self.find_optimal_times).pack(pady=20)

        # Results area for weather and activities (Equal size for both)
        self.results_text = tk.Text(self.master, height=10, width=80, bg="white", fg="black")
        self.results_text.pack(pady=10)

        # Headlines area for displaying top headlines (Equal size for both)
        ttk.Label(self.master, text="Top Headlines:", font=('times new roman', 12), background="white").pack(pady=5)
        self.news_text = tk.Text(self.master, height=10, width=80, bg="white", fg="black")
        self.news_text.pack(pady=10)

    def find_optimal_times(self):
        API_KEY = 'b732e3951546f51218c18283691d8e94'
        
        preferences = {
            'temp_min': self.temp_min.get(),
            'temp_max': self.temp_max.get(),
            'humidity_min': self.humidity_min.get(),
            'humidity_max': self.humidity_max.get(),
            'conditions': [condition for condition, var in self.condition_vars.items() if var.get()]
        }

        weather_data = fetch_weather(self.location['lat'], self.location['lon'], API_KEY)
        
        if not weather_data:
            return
        
        optimal_times = analyze_weather(weather_data, preferences)
        
        self.results_text.delete(1.0, tk.END)
        
        if optimal_times:
            self.results_text.insert(tk.END, "Optimal Times to Go Outside and Suggested Activities:\n\n")
            for time in optimal_times:
                self.results_text.insert(tk.END, f"{time['datetime']} - Temp: {time['temp']:.1f}°F, "
                                                 f"Humidity: {time['humidity']}%, Condition: {time['condition']}\n")
                if time['activities']:
                    self.results_text.insert(tk.END, "Suggested Activities:\n")
                    for activity in time['activities']:
                        self.results_text.insert(tk.END, f" - {activity}\n")
                else:
                    self.results_text.insert(tk.END, "No specific activities suggested for this time.\n")
                self.results_text.insert(tk.END, "\n")
        else:
            self.results_text.insert(tk.END, "No optimal times found based on your preferences.\n")
        
        # Fetch and display top global news headlines
        news_articles = fetch_headlines()
        
        if news_articles:
            self.news_text.delete(1.0, tk.END)
            for article in news_articles[:5]:  # Display top 5 headlines only for brevity
                title = article.get('title', 'No Title')
                description = article.get('description', 'No Description')
                self.news_text.insert(tk.END, f"Title: {title}\nDescription: {description}\n\n")
        
        else:
            self.news_text.insert(tk.END, "No news available.")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherPreferenceGUI(root)
    root.mainloop()