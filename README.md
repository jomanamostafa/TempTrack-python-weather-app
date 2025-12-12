# TempTrack-python-weather-app
A modern Python desktop weather app that displays real-time conditions, 3-day forecasts, and hourly temperature trends. Built with CustomTkinter for a sleek GUI, Matplotlib for data visualization, and Open-Meteo API for accurate weather data. Includes dynamic weather icons, emoji fallback, and city-saving functionality for personalized tracking.
**TempTrack: Python Weather Application**
Overview: TempTrack is a Python-based application designed to provide real-time weather updates in a simple and efficient manner. The project emphasizes clarity, usability, and customization, allowing users to track weather conditions for their preferred city while maintaining a lightweight structure suitable for further development or integration.
Key Features:
- Location Preferences: Users can specify their city in configuration files (my_city.txt and preferences.json).
- Weather Conditions: Supports multiple states including clear sky, partly cloudy, overcast, rain, thunderstorms, and snow.
- Real-Time Data: Retrieves current weather information using API calls.
- Visual Assets: Includes a set of weather icons stored in the images directory.
- Extensibility: Written in Python for ease of modification and future enhancements.
Project Structure: TempTrack-python-weather-app/ images/                Weather icons (PNG format) my_city.txt            User’s city preference preferences.json       User configuration settings weatherfinal.py        Main application script LICENSE                MIT License
Installation and Setup: Prerequisites:
- Python version 3.8 or higher
- Requests library for API communication
To install dependencies: pip install requests
To run the application: python weatherfinal.py
Configuration:
- Edit my_city.txt to define the default city.
- Adjust preferences.json to customize application behavior.
License: This project is distributed under the MIT License. See the LICENSE file for full details.
Future Enhancements:
- Implementation of a five-day forecast.
- Development of a graphical user interface using Tkinter or PyQt.
- Integration of multiple weather APIs for improved accuracy.
Author: Developed by Jomana Mostafa GitHub Profile: https://github.com/jomanamostafa
