import requests
from bs4 import BeautifulSoup
import os
from supabase import create_client, Client

SUPABASE_URL = "https://kdpfszinopwchmjvxdfl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtkcGZzemlub3B3Y2htanZ4ZGZsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTYyNDM0OTgsImV4cCI6MjAzMTgxOTQ5OH0.H6fs_uUEeOHjscCpqwD3MSSvLeMvsfaO9vOlbo0EDsY"

# 10 chosen location codes
location_codes = {"USNY0002:1:US", "USFL0002:1:US", "USNJ0002:1:US", "USVT0002:1:US", "USMA0002:1:US", "USNH0002:1:US", "USVA0002:1:US", "USCA0002:1:US", "USCO0002:1:US", "USUT0002:1:US"}

page = requests.get("https://weather.com/weather/today/l/USNY0002:1:US")
soup = BeautifulSoup(page.content, "html.parser")
# print(soup)

def scrape_weather_data(location_code):
    dict = {}
    page = requests.get(f"https://weather.com/weather/today/l/{location_code}")
    soup = BeautifulSoup(page.content, "html.parser")
    wx_data_div = soup.find('div', {'data-testid': 'wxData', 'class': 'WeatherDetailsListItem--wxData--kK35q'})
    temperatures = wx_data_div.find_all('span', {'data-testid': 'TemperatureValue'})

    high_temp = temperatures[0].text
    low_temp = temperatures[1].text

    location = soup.find('h1', {'class': 'CurrentConditions--location--1YWj_'}).text
    
    curr_date = date.today()

    dict["curr_date"] = date
    dict["location"] = location
    dict["high"] = high_temp
    dict["low"] = low_temp

    return dict

    # print extracted date, location, and high and low temp
    # print(f"Date: {date}")
    # print(f"Location: {location}")
    # print(f"High Temperature: {high_temp}")
    # print(f"Low Temperature: {low_temp}")

def update_tables(client, dict):
    #data, count = supabase.table('Date').insert({"date": dict.get("date")}).execute()
    #data, count = supabase.table('Location').insert({"location": dict.get("location")}).execute()
    data, count = client.table('weather').insert({"date": dict.get("date"), "location": dict.get("location"), "high": dict.get("high"), "low": dict.get("low")}).execute()

if __name__ == "__main__":
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    for location_code in location_codes:
        dict = scrape_weather_data(location_code)
        update_table(supabase, dict)
