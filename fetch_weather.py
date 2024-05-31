import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_tide_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        tides = soup.find_all('tr', class_='tide-row')
        tide_data = []
        for tide in tides:
            time = tide.find('td', class_='tide-time').text.strip()
            level = tide.find('td', class_='tide-height').text.strip()
            tide_data.append(f"{time}\t{level}")
        return tide_data
    except Exception as e:
        print(f"Error fetching tide data from {url}: {e}")
        return ["N/A"]

def fetch_sun_times(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        sunrise_elem = soup.find('p', class_='dn-mob dn-mob-d')
        sunset_elem = soup.find('p', class_='dn-mob dn-mob-n')
        if sunrise_elem and sunset_elem:
            sunrise = sunrise_elem.text.strip()
            sunset = sunset_elem.text.strip()
        else:
            raise ValueError("Could not find sunrise or sunset data.")
        return sunrise, sunset
    except Exception as e:
        print(f"Error fetching sun times from {url}: {e}")
        return "N/A", "N/A"

def fetch_weather_forecast(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        forecast_items = soup.find_all('div', class_='tombstone-container')
        forecast_data = []
        last_update_elem = soup.find('div', class_='tombstone-container')
        last_update = last_update_elem.find_previous('div').text.strip() if last_update_elem else "N/A"
        for item in forecast_items:
            period = item.find('p', class_='period-name').text
            short_desc = item.find('p', class_='short-desc').text
            temp = item.find('p', class_='temp').text
            forecast_data.append(f"{period}\n{short_desc}, {temp}")
        return forecast_data, last_update
    except Exception as e:
        print(f"Error fetching weather forecast from {url}: {e}")
        return ["N/A"], "N/A"

def format_weather_report():
    # URLs for the data
    seldovia_tides_url = 'https://tidesandcurrents.noaa.gov/noaatidepredictions.html?id=9455500&legacy=1'
    seward_tides_url = 'https://tidesandcurrents.noaa.gov/noaatidepredictions.html?id=9455090&legacy=1'
    homer_sun_url = 'https://www.timeanddate.com/sun/@5864145'
    seward_sun_url = 'https://www.timeanddate.com/sun/@7117718'
    homer_weather_url = 'https://forecast.weather.gov/MapClick.php?lat=59.6466&lon=-151.5442'
    seward_weather_url = 'https://forecast.weather.gov/MapClick.php?lat=60.1124&lon=-149.4429'
    kenai_weather_url = 'https://forecast.weather.gov/MapClick.php?zoneid=AKZ121'
    anchorage_weather_url = 'https://forecast.weather.gov/MapClick.php?lat=61.1742&lon=-149.9961'
    coastal_waters_url = 'https://tgftp.nws.noaa.gov/data/raw/fz/fzak51.pafc.cwf.aer.txt'

    # Fetch data
    seldovia_tides = fetch_tide_data(seldovia_tides_url)
    seward_tides = fetch_tide_data(seward_tides_url)
    sunrise_homer, sunset_homer = fetch_sun_times(homer_sun_url)
    sunrise_seward, sunset_seward = fetch_sun_times(seward_sun_url)
    weather_homer, last_update_homer = fetch_weather_forecast(homer_weather_url)
    weather_seward, last_update_seward = fetch_weather_forecast(seward_weather_url)
    weather_kenai, last_update_kenai = fetch_weather_forecast(kenai_weather_url)
    weather_anchorage, last_update_anchorage = fetch_weather_forecast(anchorage_weather_url)

    # Format report
    report = f"""
    WEATHER for:
    KBBI Homer AM 890
    K201AO Seward 88.1 FM
    {datetime.now().strftime('%A %B %d')}
    
    Seldovia District Tides:
    {'\n'.join(seldovia_tides)}
    
    Seward District Tides:
    {'\n'.join(seward_tides)}
    
    Homer Sunrise/Sunset
    Sunrise: {sunrise_homer}
    Sunset: {sunset_homer}
    
    Seward Sunrise/Sunset
    Sunrise: {sunrise_seward}
    Sunset: {sunset_seward}
    
    ________________________________________________________________________________
    Homer
    Last update: {last_update_homer}
    
    {'\n'.join(weather_homer)}
    --------------------------------------------------------------------------------
    Seward
    Last update: {last_update_seward}
    
    {'\n'.join(weather_seward)}
    ________________________________________________________________________________
    Western Kenai Peninsula
    Last update: {last_update_kenai}
    
    {'\n'.join(weather_kenai)}
    --------------------------------------------------------------------------------
    Anchorage
    Last update: {last_update_anchorage}
    
    {'\n'.join(weather_anchorage)}
    ________________________________________________________________________________
    Coastal Waters Forecast
    National Weather Service Anchorage Alaska
    {datetime.now().strftime('%I:%M %p %A %B %d %Y')}
    {requests.get(coastal_waters_url).text}
    """
    return report

def main():
    report = format_weather_report()
    with open('weather.txt', 'w') as file:
        file.write(report)

if __name__ == "__main__":
    main()
