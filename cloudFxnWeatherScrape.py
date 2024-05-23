import functions_framework
import requests
from bs4 import BeautifulSoup
import os
from supabase import create_client, Client
from datetime import datetime


SUPABASE_URL = "" # fill in with url associated w supabase db
SUPABASE_KEY = "" # fill in with key associated w supabase db

# Stores chosen location codes
location_codes = []

def scrape_weather_data_update_weather_table(client, date, location_code):
    """
    Populates the weather table with location code, date id and associated high and low temperaturs (obtained through web scraping). Intends to be run once daily.
    
    Parameters
    -------
    client: Client 
        Connection to supabase database
    date: string
    location_code: string

    Returns
    -------
    void
    """
    page = requests.get(f"https://weather.com/weather/today/l/{location_code}")
    soup = BeautifulSoup(page.content, "html.parser")

    # Version 1: High temp tends to be null 
    # wx_data_div = soup.find('div', {'data-testid': 'wxData', 'class': 'WeatherDetailsListItem--wxData--kK35q'})
    # temperatures = wx_data_div.find_all('span', {'data-testid': 'TemperatureValue'})
    
    # Version 2: High temp does not tend to be null
    temperatures = soup.find_all('span', {'data-testid': 'TemperatureValue'})

    high_temp = temperatures[0].text
    low_temp = temperatures[1].text  

    update_weather_table(client, get_date_id(client, date), location_code, format_temp(high_temp), format_temp(low_temp))

def init_location_table(client, location_codeslcl):
    """
    Populates the location table with location codes and associated location names (using web scraping). Intends to be run once ever.
    
    Parameters
    -------
    client: Client 
        Connection to supabase database
    location_codeslcl: list[string]
        Chosen location codes to track weather data for

    Returns
    -------
    void
    """
    for location_code in location_codeslcl:
        page = requests.get(f"https://weather.com/weather/today/l/{location_code}")
        soup = BeautifulSoup(page.content, "html.parser")

        location = soup.find('h1', {'class': 'CurrentConditions--location--1YWj_'}).text
        update_location_table(client, location_code, location)

def populate_global_location_codes(client):
    """
    Populates the global variable ``location-codes`` with the valeus stored in the location table. 
    
    Parameters
    -------
    client: Client 
        Connection to supabase database

    Returns
    -------
    void
    """
    data,count = client.from_('location_table').select('location_code').execute()
    for i in range(len(data[1])):
        print(data[1][i].get("location_code"))
        location_codes.append(data[1][i].get("location_code"))
    print(location_codes)

# Functions that update each table
def update_weather_table(client, date_id, location_code, high_temp, low_temp):
    """
    Insert row to weather table containing date_id, location_code, high_temp, and low_temp

    Parameters
    -------
    client: Client 
        Connection to supabase database
    date: string
        Date associated with date_id
    location_code: string
        Location code 
    high_temp: int
        High temp per location per date
    low_temp: int
        Low temp per location per date

    Returns
    -------
    void
    """
    response = client.table('weather_table').insert({"date_id": date_id, "location_code": location_code, "high": high_temp, "low": low_temp}).execute()

def update_location_table(client, location_code, location_name): 
    """
    Insert row to location table containing location_code and location_name

    Parameters
    -------
    client: Client 
        Connection to supabase database
    location_code: string
    location_name: string

    Returns
    -------
    void
    """
    data, count = client.table('location_table').insert({"location_code": location_code, "location_name": location_name}).execute()

def update_date_table(client, date): 
    """
    Insert row to location table containing date (date_id is autoincremented)
    Parameters
    -------
    client: Client 
        Connection to supabase database
    date: string

    Returns
    -------
    void
    """
    data, count = client.table('date_table').insert({"date": date}).execute()

# Helper functions
def get_todays_date():
    """
    Get today's date. 

    Returns
    -------
    string
        Today's date in "%Y-%m-%d" format
    """
    return datetime.now().strftime("%Y-%m-%d"); 

def get_date_id(client, date):
    """
    Get date_id assoicated with ``date``. 

    Parameters
    -------
    client: Client 
        Connection to supabase database
    date: string
        string representation of date

    Returns
    -------
    int
        date_id associated with ``date``
    """
    data,count = client.from_('date_table').select('date_id').eq('date', date).execute()
    return int(data[1][0].get("date_id"))

def format_temp(unformatted_temp):
    """
    Format string representation of temperature.   

    Parameters
    -------
    unformatted_temp: string 

    Returns
    -------
    int
        formatted integer representation of temperature
    """
    if (unformatted_temp == "--"):
        formatted_temp = None
    else:
        # Get rid of degree sign and cast to int
        formatted_temp = int(unformatted_temp[:-1])
    return formatted_temp

# Used for testing, ran once ever before cloud func is deployed
def setup(client):
    init_location_table(client, ["USNY0002:1:US", "USFL0002:1:US", "USNJ0002:1:US", "USVT0002:1:US", "USMA0002:1:US", "USNH0002:1:US", "USVA0002:1:US", "USCA0002:1:US", "USCO0002:1:US", "USUT0002:1:US"])

#Ran daily
@functions_framework.http
def main(request):
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    date = get_todays_date()
    update_date_table(supabase, date)
    populate_global_location_codes(supabase)
    for location_code in location_codes:
        scrape_weather_data_update_weather_table(supabase, date, location_code)
    return "Database has been updated"