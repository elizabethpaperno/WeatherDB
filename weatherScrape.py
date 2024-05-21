import requests
from bs4 import BeautifulSoup

location_codes = {"USNY0002:1:US"}

page = requests.get("https://weather.com/weather/today/l/USNY0002:1:US")
soup = BeautifulSoup(page.content, "html.parser")
print(soup)