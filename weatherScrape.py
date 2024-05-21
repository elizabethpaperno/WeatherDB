import requests
from bs4 import BeautifulSoup

# 10 chosen location codes
location_codes = {"USNY0002:1:US", "USFL0002:1:US", "USNJ0002:1:US", "USVT0002:1:US", "USMA0002:1:US", "USNH0002:1:US", "USVA0002:1:US", "USCA0002:1:US", "USCO0002:1:US", "USUT0002:1:US"}

page = requests.get("https://weather.com/weather/today/l/USNY0002:1:US")
soup = BeautifulSoup(page.content, "html.parser")
# print(soup)

for location_code in location_codes:
    page = requests.get(f"https://weather.com/weather/today/l/{location_code}")
    soup = BeautifulSoup(page.content, "html.parser")
    wx_data_div = soup.find('div', {'data-testid': 'wxData', 'class': 'WeatherDetailsListItem--wxData--kK35q'})
    temperatures = wx_data_div.find_all('span', {'data-testid': 'TemperatureValue'})

    high_temp = temperatures[0].text
    low_temp = temperatures[1].text

    location = soup.find('h1', {'class': 'CurrentConditions--location--1YWj_'}).text
    
    date = date.today()

    # print extracted date, location, and high and low temp
    print(f"Date: {date}")
    print(f"Location: {location}")
    print(f"High Temperature: {high_temp}")
    print(f"Low Temperature: {low_temp}")