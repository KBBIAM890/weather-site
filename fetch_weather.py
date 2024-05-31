import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_tides(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tides = soup.find_all('tr', class_='pred-line')
    tides_data = []
    for tide in tides:
        columns = tide.find_all('td')
        if len(columns) >= 3:
            time = columns[1].text.strip()
            height = columns[2].text.strip()
            tides_data.append(f"{time}\t{height}")
    return tides_data

def fetch_sun_times(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    sunrise_elem = soup.find('span', {'id': 'sunrise'})
    sunset_elem = soup.find('span', {'id': 'sunset'})

    sunrise = sunrise_elem.text.strip() if sunrise_elem else "N/A"
    sunset = sunset_elem.text.strip() if sunset_elem else "N/A"

    return sunrise, sunset

def fetch_weather_forecast(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    forecast = soup.find_all('div', class_='tombstone-container')
    last_update_elem = soup.find('div', class_='tombstone-container').find_previous('div')
    last_update = last_update_elem.text.strip() if last_update_elem else "N/A"
    weather_data = []
    for period in forecast:
        period_name = period.find('p', class_='period-name').text.strip()
        short_desc = period.find('p', class_='short-desc').text.strip()
        temp = period.find('p', class_='temp').text.strip()
        weather_data.append(f"{period_name}\n{short_desc}, {temp}")
    return weather_data, last_update

def fetch_coastal_forecast(url):
    response = requests.get(url)
    return response.text.strip()

def main():
    tides_seldovia = fetch_tides('https://tidesandcurrents.noaa.gov/noaatidepredictions.html?id=9455500&legacy=1')
    tides_seward = fetch_tides('https://tidesandcurrents.noaa.gov/noaatidepredictions.html?id=9455090&legacy=1')
    sunrise_sunset_homer = fetch_sun_times('https://www.timeanddate.com/sun/@5864145')
    sunrise_sunset_seward = fetch_sun_times('https://www.timeanddate.com/sun/@7117718')
    weather_homer, last_update_homer = fetch_weather_forecast('https://forecast.weather.gov/MapClick.php?lat=59.6466&lon=-151.5442')
    weather_seward, last_update_seward = fetch_weather_forecast('https://forecast.weather.gov/MapClick.php?lat=60.1124&lon=-149.4429')
    weather_kenai, last_update_kenai = fetch_weather_forecast('https://forecast.weather.gov/MapClick.php?zoneid=AKZ121')
    weather_anchorage, last_update_anchorage = fetch_weather_forecast('https://forecast.weather.gov/MapClick.php?lat=61.1742&lon=-149.9961')
    coastal_forecast = fetch_coastal_forecast('https://tgftp.nws.noaa.gov/data/raw/fz/fzak51.pafc.cwf.aer.txt')

    weather_report = f"""
    WEATHER for:
    KBBI Homer AM 890
    K201AO Seward 88.1 FM
    {datetime.now().strftime('%A %B %d')}

    Seldovia District Tides:
    Low Tide: {tides_seldovia[0] if len(tides_seldovia) > 0 else 'N/A'}
    High Tide: {tides_seldovia[1] if len(tides_seldovia) > 1 else 'N/A'}

    Seward District Tides:
    Low Tide: {tides_seward[0] if len(tides_seward) > 0 else 'N/A'}
    High Tide: {tides_seward[1] if len(tides_seward) > 1 else 'N/A'}

    Homer Sunrise/Sunset
    Sunrise: {sunrise_sunset_homer[0]}
    Sunset: {sunrise_sunset_homer[1]}

    Seward Sunrise/Sunset
    Sunrise: {sunrise_sunset_seward[0]}
    Sunset: {sunrise_sunset_seward[1]}

    {"_"*80}
    Homer
    {"\n".join(weather_homer)}
    Last Update: {last_update_homer}

    {"-"*80}
    Seward
    {"\n".join(weather_seward)}
    Last Update: {last_update_seward}

    {"_"*80}
    Western Kenai Peninsula
    {"\n".join(weather_kenai)}
    Last Update: {last_update_kenai}

    {"-"*80}
    Anchorage
    {"\n".join(weather_anchorage)}
    Last Update: {last_update_anchorage}

    {"_"*80}
    Coastal Waters Forecast
    National Weather Service Anchorage Alaska
    {datetime.now().strftime('%I:%M %p %Z %A %B %d %Y')}
    {coastal_forecast}

    {"_"*80}

    Seldovia District Tides:
    High Tide: {tides_seldovia[2] if len(tides_seldovia) > 2 else 'N/A'}
    Low Tide: {tides_seldovia[3] if len(tides_seldovia) > 3 else 'N/A'}

    Seward District Tides:
    High Tide: {tides_seward[2] if len(tides_seward) > 2 else 'N/A'}
    Low Tide: {tides_seward[3] if len(tides_seward) > 3 else 'N/A'}

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
