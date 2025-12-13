import customtkinter as ctk
from tkinter import messagebox
import urllib.request
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

# deh hena 3l4an law elly byrun el code ma3mal4 install l PIL fa elimgs me4 hate4ta8al fa sa3etha use text emojis 3ady w ana 7atetha fe else in a function law el img me4 mawgoda
try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except:
    HAS_PIL = False

# bg color lazem 6 char hexadecimal only
bg_color = "#0000ff"
text_color = "white"

# weather describtion
weather_meaning = {
    0: "Clear sky",
    1: "Clear sky",
    2: "Clear sky",
    3: "Clear sky",
    4: "Clear sky",
    5: "Clear sky",
    6: "Clear sky",
    7: "Clear sky",
    8: "Clear sky",
    9: "Clear sky",
    10: "Clear sky",
    11: "Mostly clear",
    12: "Mostly clear",
    13: "Mostly clear",
    14: "Mostly clear",
    15: "Mostly clear",
    16: "Mostly clear",
    17: "Mostly clear",
    18: "Mostly clear",
    19: "Mostly clear",
    20: "Mostly clear",
    21: "Partly cloudy",
    22: "Partly cloudy",
    23: "Partly cloudy",
    24: "Partly cloudy",
    25: "Partly cloudy",
    26: "Partly cloudy",
    27: "Partly cloudy",
    28: "Partly cloudy",
    29: "Partly cloudy",
    30: "Partly cloudy",
    31: "Partly cloudy",
    32: "Partly cloudy",
    33: "Partly cloudy",
    34: "Partly cloudy",
    35: "Partly cloudy",
    36: "Partly cloudy",
    37: "Partly cloudy",
    38: "Partly cloudy",
    39: "Partly cloudy",
    40: "Partly cloudy",
    41: "Cloudy",
    42: "Cloudy",
    43: "Cloudy",
    44: "Cloudy",
    45: "Cloudy",
    46: "Cloudy",
    47: "Cloudy",
    48: "Cloudy",
    49: "Cloudy",
    50: "Cloudy",
    51: "Cloudy",
    52: "Cloudy",
    53: "Cloudy",
    54: "Cloudy",
    55: "Cloudy",
    56: "Cloudy",
    57: "Cloudy",
    58: "Cloudy",
    59: "Cloudy",
    60: "Cloudy",
    61: "Rain",
    62: "Rain",
    63: "Rain",
    64: "Rain",
    65: "Rain",
    66: "Rain",
    67: "Rain",
    68: "Rain",
    69: "Rain",
    70: "Rain",
    71: "Snow",
    72: "Snow",
    73: "Snow",
    74: "Snow",
    75: "Snow",
    76: "Snow",
    77: "Snow",
    78: "Snow",
    79: "Snow",
    80: "Snow",
    81: "Snow",
    82: "Snow",
    83: "Snow",
    84: "Snow",
    85: "Snow",
    86: "Snow",
    87: "Snow",
    88: "Snow",
    89: "Snow",
    90: "Snow",
    91: "Snow",
    92: "Snow",
    93: "Snow",
    94: "Snow",
    95: "Thunder",
    96: "Thunder",
    97: "Thunder",
    98: "Thunder",
    99: "Thunder",
    100: "Thunder"
}

# global stuff
current_weather_code = 0
graph_widget = None

# current weather
def get_current_weather(city_name):
    global current_weather_code
    try:
        url1 = "https://geocoding-api.open-meteo.com/v1/search?name=" + city_name + "&count=1"
        response1 = urllib.request.urlopen(url1)
        data1 = json.loads(response1.read())
        if len(data1.get("results", [])) == 0:
            return "City not found!"
        
        lat = data1["results"][0]["latitude"]
        lon = data1["results"][0]["longitude"]

        url2 = "https://api.open-meteo.com/v1/forecast?latitude=" + str(lat) + "&longitude=" + str(lon) + "&current_weather=true"
        response2 = urllib.request.urlopen(url2)
        data2 = json.loads(response2.read())

        current = data2["current_weather"]
        current_weather_code = current["weathercode"]
        temp = current["temperature"]
        description = weather_meaning.get(current_weather_code, "Unknown")
        return city_name.upper() + "\n" + str(temp) + "°C" + "\n" + description
    except:
        return "Error getting weather."

#forecast for next 3 days
def get_forecast(city_name):
    try:
        url1 = "https://geocoding-api.open-meteo.com/v1/search?name=" + city_name + "&count=1"
        response1 = urllib.request.urlopen(url1)
        data1 = json.loads(response1.read())
        if len(data1.get("results", [])) == 0:
            return "City not found."

        lat = data1["results"][0]["latitude"]
        lon = data1["results"][0]["longitude"]

        url2 = "https://api.open-meteo.com/v1/forecast?latitude=" + str(lat) + "&longitude=" + str(lon) + "&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=auto"
        response2 = urllib.request.urlopen(url2)
        data2 = json.loads(response2.read())

        daily = data2["daily"]
        result = "Next 3 days:\n"
        for i in range(3):
            date = daily["time"][i]
            tmin = daily["temperature_2m_min"][i]
            tmax = daily["temperature_2m_max"][i]
            code = daily["weathercode"][i]
            desc = weather_meaning.get(code, "???")
            result += date + ": " + desc + ", " + str(tmin) + " to " + str(tmax) + "°C\n"
        return result
    except:
        return "Error getting forecast."

# dah graph bet4ow el temp per hour in the current date
def draw_graph(city_name):
    global graph_widget
    try:
        url1 = "https://geocoding-api.open-meteo.com/v1/search?name=" + city_name + "&count=1"
        response1 = urllib.request.urlopen(url1)
        data1 = json.loads(response1.read())
        if len(data1.get("results", [])) == 0:
            messagebox.showerror("Error", "City not found")
            return

        lat = data1["results"][0]["latitude"]
        lon = data1["results"][0]["longitude"]

        url2 = "https://api.open-meteo.com/v1/forecast?latitude=" + str(lat) + "&longitude=" + str(lon) + "&hourly=temperature_2m&timezone=auto"
        response2 = urllib.request.urlopen(url2)
        data2 = json.loads(response2.read())

        times = data2["hourly"]["time"][:24]
        temps = data2["hourly"]["temperature_2m"][:24]

        x_labels = []
        x_positions = []
        for i in range(0, 24, 3):
            full_time = times[i]
            hour_part = full_time.split("T")[1]
            hour_number = hour_part.split(":")[0]
            x_labels.append(hour_number + "h")
            x_positions.append(i)

        plt.style.use('default')
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)

        ax.plot(temps, color="cyan", linewidth=2)
        ax.set_xticks(x_positions)
        ax.set_xticklabels(x_labels)

        ax.set_title(city_name + " - Today", color=text_color, fontname="Verdana",fontweight="bold")
        ax.set_ylabel("Temp (°C)", color=text_color, fontname="Verdana", fontweight="bold")
        ax.set_xlabel("Time", color=text_color, fontname="Verdana", fontweight="bold")
        ax.tick_params(colors=text_color)
        for label in ax.get_xticklabels():
            label.set_fontname("Verdana")
        for label in ax.get_yticklabels():
            label.set_fontname("Verdana")
        ax.grid(True, color="gray", alpha=0.3)

        if graph_widget is not None:
            graph_widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=graph_area)
        canvas.draw()
        graph_widget = canvas.get_tk_widget()
        graph_widget.pack(expand=True, fill="both")

    except:
        pass

#ICON DISPLAY FUNCTION
def show_icon():
    icon_map = {
        0: "images/Clear Sky.png",
        1: "images/Clear Sky.png",
        2: "images/Clear Sky.png",
        3: "images/Clear Sky.png",
        4: "images/Clear Sky.png",
        5: "images/Clear Sky.png",
        6: "images/Clear Sky.png",
        7: "images/Clear Sky.png",
        8: "images/Clear Sky.png",
        9: "images/Clear Sky.png",
        10: "images/Clear Sky.png",
        11: "images/Mainly Clear.png",
        12: "images/Mainly Clear.png",
        13: "images/Mainly Clear.png",
        14: "images/Mainly Clear.png",
        15: "images/Mainly Clear.png",
        16: "images/Mainly Clear.png",
        17: "images/Mainly Clear.png",
        18: "images/Mainly Clear.png",
        19: "images/Mainly Clear.png",
        20: "images/Mainly Clear.png",
        21: "images/Partly Cloudy.png",
        22: "images/Partly Cloudy.png",
        23: "images/Partly Cloudy.png",
        24: "images/Partly Cloudy.png",
        25: "images/Partly Cloudy.png",
        26: "images/Partly Cloudy.png",
        27: "images/Partly Cloudy.png",
        28: "images/Partly Cloudy.png",
        29: "images/Partly Cloudy.png",
        30: "images/Partly Cloudy.png",
        31: "images/Partly Cloudy.png",
        32: "images/Partly Cloudy.png",
        33: "images/Partly Cloudy.png",
        34: "images/Partly Cloudy.png",
        35: "images/Partly Cloudy.png",
        36: "images/Partly Cloudy.png",
        37: "images/Partly Cloudy.png",
        38: "images/Partly Cloudy.png",
        39: "images/Partly Cloudy.png",
        40: "images/Partly Cloudy.png",
        41: "images/Overcast.png",
        42: "images/Overcast.png",
        43: "images/Overcast.png",
        44: "images/Overcast.png",
        45: "images/Overcast.png",
        46: "images/Overcast.png",
        47: "images/Overcast.png",
        48: "images/Overcast.png",
        49: "images/Overcast.png",
        50: "images/Overcast.png",
        51: "images/Overcast.png",
        52: "images/Overcast.png",
        53: "images/Overcast.png",
        54: "images/Overcast.png",
        55: "images/Overcast.png",
        56: "images/Overcast.png",
        57: "images/Overcast.png",
        58: "images/Overcast.png",
        59: "images/Overcast.png",
        60: "images/Overcast.png",
        61: "images/Rain .png",
        62: "images/Rain .png",
        63: "images/Rain .png",
        64: "images/Rain .png",
        65: "images/Rain .png",
        66: "images/Rain .png",
        67: "images/Rain .png",
        68: "images/Rain .png",
        69: "images/Rain .png",
        70: "images/Rain .png",
        71: "images/snow.png",
        72: "images/snow.png",
        73: "images/snow.png",
        74: "images/snow.png",
        75: "images/snow.png",
        76: "images/snow.png",
        77: "images/snow.png",
        78: "images/snow.png",
        79: "images/snow.png",
        80: "images/snow.png",
        81: "images/snow.png",
        82: "images/snow.png",
        83: "images/snow.png",
        84: "images/snow.png",
        85: "images/snow.png",
        86: "images/snow.png",
        87: "images/snow.png",
        88: "images/snow.png",
        89: "images/snow.png",
        90: "images/snow.png",
        91: "images/snow.png",
        92: "images/snow.png",
        93: "images/snow.png",
        94: "images/snow.png",
        95: "images/Thunderstorm.png",
        96: "images/Thunderstorm.png",
        97: "images/Thunderstorm.png",
        98: "images/Thunderstorm.png",
        99: "images/Thunderstorm.png",
        100: "images/Thunderstorm.png"
    }
    path = icon_map.get(current_weather_code, "images/sun.png")
    
    if HAS_PIL:
        try:
            img = Image.open(path)
            img = img.resize((200, 200))
            photo = ImageTk.PhotoImage(img)
            icon_label.configure(image=photo, text="")
            icon_label.image = photo 
        except:
            icon_label.configure(image="", text="🌤️", font=("Verdana", 60))
    else:
        # fallback to emoji if PIL missing
        emoji_map = {0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️", 61: "🌧️", 71: "❄️", 95: "⛈️"}
        emoji = emoji_map.get(current_weather_code, "🌤️")
        icon_label.configure(image="", text=emoji, font=("Verdana", 60))

# save city
def save_favorite():
    city = entry_city.get()
    if city:
        try:
            f = open("my_city.txt", "w")
            f.write(city)
            f.close()
            messagebox.showinfo("Saved!", "Your city is saved!")
        except:
            pass

def load_favorite():
    try:
        f = open("my_city.txt", "r")
        city = f.read().strip()
        f.close()
        entry_city.delete(0, "end")
        entry_city.insert(0, city)
        get_weather_and_graph()
    except:
        messagebox.showinfo("Info", "No saved city.")

def go_home():
    global graph_widget
    entry_city.delete(0, "end")
    label_result.configure(text="Enter a city")
    icon_label.configure(image="", text="")
    if graph_widget is not None:
        graph_widget.destroy()
        graph_widget = None

def get_weather_and_graph():
    city = entry_city.get().strip()
    if city == "":
        messagebox.showwarning("Wait!", "Please type a city name.")
        return

    label_result.configure(text="Loading...")
    result1 = get_current_weather(city)
    result2 = get_forecast(city)
    full_text = result1 + "\n\n" + result2
    label_result.configure(text=full_text)
    show_icon()       
    draw_graph(city)

#WINDOW
ctk.set_appearance_mode("dark")#momken ne5aly light law haben bas me4 hykon zaref w keda keda me4 hatban 3l4an 7atet color style fe mo3zam el hagat
window = ctk.CTk()
window.title("My Weather App")
window.geometry("900x650")
window.configure(fg_color=bg_color)

label_top = ctk.CTkLabel(window, text="Welcome to TempTrack", font=("Verdana", 35, "bold"), text_color=text_color)
label_top.pack(pady=10)

frame_input = ctk.CTkFrame(window, fg_color=bg_color)
frame_input.pack(pady=10)

entry_city = ctk.CTkEntry(frame_input,fg_color="white", width=250,text_color="#0000ff", placeholder_text="Enter city", font=("Verdana", 20,"bold"))
entry_city.pack(side="left", padx=5)

button_get = ctk.CTkButton(frame_input,text_color="#0000ff",fg_color="yellow", text="Get Weather", command=get_weather_and_graph, font=("Verdana",18,"bold"))
button_get.pack(side="left", padx=5)

frame_buttons = ctk.CTkFrame(window, fg_color=bg_color)
frame_buttons.pack(pady=5)

ctk.CTkButton(frame_buttons,fg_color="black",text_color="white", text="Home", command=go_home, font=("Verdana",15,"bold")).pack(side="left", padx=3)
ctk.CTkButton(frame_buttons,fg_color="black",text_color="white", text="Save City", command=save_favorite, font=("Verdana", 15,"bold")).pack(side="left", padx=3)
ctk.CTkButton(frame_buttons,fg_color="black",text_color="white", text="Load Saved", command=load_favorite, font=("Verdana",15,"bold")).pack(side="left", padx=3)

#ICON LABEL
icon_label = ctk.CTkLabel(window, text="", fg_color="transparent")
icon_label.pack(pady=10)

label_result = ctk.CTkLabel(window, text="Enter a city to start", font=("Verdana",18,"bold"), text_color=text_color, wraplength=400, justify="center")
label_result.pack(pady=8)

graph_area = ctk.CTkFrame(window, fg_color=bg_color, height=250)
graph_area.pack(pady=10, fill="x", padx=20)
graph_area.pack_propagate(False)

window.mainloop()