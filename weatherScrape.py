import requests
from bs4 import BeautifulSoup
import os
from supabase import create_client, Client
from datetime import datetime


SUPABASE_URL = "https://kdpfszinopwchmjvxdfl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtkcGZzemlub3B3Y2htanZ4ZGZsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTYyNDM0OTgsImV4cCI6MjAzMTgxOTQ5OH0.H6fs_uUEeOHjscCpqwD3MSSvLeMvsfaO9vOlbo0EDsY"

# 10 chosen location codes
location_codes = {"USNY0002:1:US", "USFL0002:1:US", "USNJ0002:1:US", "USVT0002:1:US", "USMA0002:1:US", "USNH0002:1:US", "USVA0002:1:US", "USCA0002:1:US", "USCO0002:1:US", "USUT0002:1:US"}

page = requests.get("https://weather.com/weather/today/l/USNY0002:1:US")
soup = BeautifulSoup(page.content, "html.parser")
# print(soup)

def scrape_weather_data(client, location_code):
    dict = {}
    page = requests.get(f"https://weather.com/weather/today/l/{location_code}")
    soup = BeautifulSoup(page.content, "html.parser")
    wx_data_div = soup.find('div', {'data-testid': 'wxData', 'class': 'WeatherDetailsListItem--wxData--kK35q'})
    temperatures = wx_data_div.find_all('span', {'data-testid': 'TemperatureValue'})

    high_temp = temperatures[0].text
    low_temp = temperatures[1].text

    location = soup.find('h1', {'class': 'CurrentConditions--location--1YWj_'}).text
    
    date = datetime.now().strftime("%Y-%m-%d")

    try:
        update_date_table(client, date)
    except: 
        # means date has already been added, ignore error
        pass  

    try: 
        update_location_table(client, location_code, location)  
    except: 
         # means location has already been added, ignore error
        pass

    update_weather_table(client, date, location_code, high_temp, low_temp)

    # print extracted date, location, and high and low temp
    # print(f"Date: {date}")
    # print(f"Location: {location}")
    # print(f"High Temperature: {high_temp}")
    # print(f"Low Temperature: {low_temp}")

def format_temp(unformatted_temp):
    if (unformatted_temp == "--"):
        formatted_temp = None
    else:
        # get rid of degree sign and cast to int
        formatted_temp = int(unformatted_temp[:-1])
    return formatted_temp

def update_weather_table(client, date_id, location_code, high_temp, low_temp):
    # data,count = client.from('date')
    #     .select('date')
    #     .eq(dict.get("date"))
    #     .execute()
    data, count = client.table('weather').insert({"date_id": date_id, "location_code": location_code, "high": high_temp, "low": low_temp}).execute()

def update_location_table(client, location_code, location_name): 
    data, count = supabase.table('location').insert({"id": dict.get("location_code"), "location_name": dict.get("location")}).execute()

def update_date_table(client, date): 
    data, count = supabase.table('date').insert({"date": dict.get("date")}).execute()
    

if __name__ == "__main__":
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    count = 0
    for location_code in location_codes:
        scrape_weather_data(location_code)
