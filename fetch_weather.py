import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_tides(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tides = soup.find_all('tr', class_='pred-line')
    tides_data = []
    for tide in tides:
        time = tide.find_all('td')[1].text.strip()
        height = tide.find_all('td')[2].text.strip()
        tides_data.append(f"{time}\t{height}")
    return tides_data

def fetch_sun_times(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    sunrise = soup.find('p', class_='dn-mob dn-mob-d').text.strip()
    sunset = soup.find('p', class_='dn-mob dn-mob-n').text.strip()
    return sunrise, sunset

def fetch_weather_forecast(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    forecast = soup.find_all('div', class_='row-forecast')
    weather_data = []
    for period in forecast:
        period_name = period.find('div', class_='col-sm-2 forecast-label').text.strip()
        period_desc = period.find('div', class_='col-sm-10 forecast-text').text.strip()
        weather_data.append(f"{period_name}\n{period_desc}")
    return weather_data

def fetch_coastal_forecast(url):
    response = requests.get(url)
    return response.text.strip()

def main():
    tides_seldovia = fetch_tides('https://tidesandcurrents.noaa.gov/noaatidepredictions.html?id=9455500&legacy=1')
    tides_seward = fetch_tides('https://tidesandcurrents.noaa.gov/noaatidepredictions.html?id=9455090&legacy=1')
    sunrise_sunset_homer = fetch_sun_times('https://www.timeanddate.com/sun/@5864145')
    sunrise_sunset_seward = fetch_sun_times('https://www.timeanddate.com/sun/@7117718')
    weather_homer = fetch_weather_forecast('https://forecast.weather.gov/MapClick.php?lat=59.6466&lon=-151.5442')
    weather_seward = fetch_weather_forecast('https://forecast.weather.gov/MapClick.php?lat=60.1124&lon=-149.4429')
    weather_kenai = fetch_weather_forecast('https://forecast.weather.gov/MapClick.php?zoneid=AKZ121')
    weather_anchorage = fetch_weather_forecast('https://forecast.weather.gov/MapClick.php?lat=61.1742&lon=-149.9961')
    coastal_forecast = fetch_coastal_forecast('https://tgftp.nws.noaa.gov/data/raw/fz/fzak51.pafc.cwf.aer.txt')

    weather_report = f"""
    WEATHER for:
    KBBI Homer AM 890
    K201AO Seward 88.1 FM
    {datetime.now().strftime('%A %B %d')}


    Seldovia District Tides:
    Low Tide: {tides_seldovia[0]}
    High Tide: {tides_seldovia[1]}


    Seward District Tides:
    Low Tide: {tides_seward[0]}
    High Tide: {tides_seward[1]}


    Homer Sunrise/Sunset
    Sunrise: {sunrise_sunset_homer[0]}
    Sunset: {sunrise_sunset_homer[1]}


    Seward Sunrise/Sunset
    Sunrise: {sunrise_sunset_seward[0]}
    Sunset: {sunrise_sunset_seward[1]}

    {"_"*80}
    Homer
    {"\n".join(weather_homer)}

    {"-"*80}
    Seward
    {"\n".join(weather_seward)}

    {"_"*80}
    Western Kenai Peninsula
    {"\n".join(weather_kenai)}

    {"-"*80}
    Anchorage
    {"\n".join(weather_anchorage)}

    {"_"*80}
    Coastal Waters Forecast
    National Weather Service Anchorage Alaska
    {datetime.now().strftime('%I:%M %p %Z %A %B %d %Y')}
    {coastal_forecast}

    {"_"*80}

    Seldovia District Tides:
    High Tide: {tides_seldovia[2]}
    Low Tide: {tides_seldovia[3]}

    Seward District Tides:
    High Tide: {tides_seward[2]}
    Low Tide: {tides_seward[3]}

    Homer Sunrise/Sunset
    Sunrise: {sunrise_sunset_homer[0]}
    Sunset: {sunrise_sunset_homer[1]}

    Seward Sunrise/Sunset
    Sunrise: {sunrise_sunset_seward[0]}
    Sunset: {sunrise_sunset_seward[1]}
    """

    with open('weather.txt', 'w') as file:
        file.write(weather_report.strip())

if __name__ == '__main__':
    main()
