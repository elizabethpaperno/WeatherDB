import requests
from bs4 import BeautifulSoup

location_codes = {"USNY0002:1:US"}

page = requests.get("https://weather.com/weather/today/l/USNY0002:1:US")
soup = BeautifulSoup(page.content, "html.parser")
# print(soup)

wx_data_div = soup.find('div', {'data-testid': 'wxData', 'class': 'WeatherDetailsListItem--wxData--kK35q'})
temperatures = wx_data_div.find_all('span', {'data-testid': 'TemperatureValue'})
high_temp = temperatures[0].text
low_temp = temperatures[1].text

# print extracted high and low temp
print(f"High Temperature: {high_temp}")
print(f"Low Temperature: {low_temp}")