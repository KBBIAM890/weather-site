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
            forecast_data.append(f"{period}\n{short_desc}. {temp}")
        return forecast_data, last_update
    except Exception as e:
        print(f"Error fetching weather forecast from {url}: {e}")
        return ["N/A"], "N/A"

def fetch_coastal_forecast(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching coastal waters forecast from {url}: {e}")
        return "N/A"

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
    coastal_waters_forecast = fetch_coastal_forecast(coastal_waters_url)

    # Format report
    report = f"""
WEATHER for:
KBBI Homer AM 890
K201AO Seward 88.1 FM
{datetime.now().strftime('%A %B %d')}

Seldovia District Tides:
Low Tide: {seldovia_tides[0] if len(seldovia_tides) > 0 else 'N/A'}
High Tide: {seldovia_tides[1] if len(seldovia_tides) > 1 else 'N/A'}

Seward District Tides:
Low Tide: {seward_tides[0] if len(seward_tides) > 0 else 'N/A'}
High Tide: {seward_tides[1] if len(seward_tides) > 1 else 'N/A'}

Homer Sunrise/Sunset
Sunrise: {sunrise_homer}
Sunset: {sunset_homer}

Seward Sunrise/Sunset
Sunrise: {sunrise_seward}
Sunset: {sunset_seward}

_______________________________________________________________
Homer 
Last update: {last_update_homer}

{weather_homer[0] if len(weather_homer) > 0 else 'N/A'}
{weather_homer[1] if len(weather_homer) > 1 else 'N/A'}
{weather_homer[2] if len(weather_homer) > 2 else 'N/A'}
{weather_homer[3] if len(weather_homer) > 3 else 'N/A'}

----------------------------------------------------------------------------------------------
Seward 
Last update: {last_update_seward}

{weather_seward[0] if len(weather_seward) > 0 else 'N/A'}
{weather_seward[1] if len(weather_seward) > 1 else 'N/A'}
{weather_seward[2] if len(weather_seward) > 2 else 'N/A'}
{weather_seward[3] if len(weather_seward) > 3 else 'N/A'}

_______________________________________________________________________________
Western Kenai Peninsula
Last update: {last_update_kenai}

{weather_kenai[0] if len(weather_kenai) > 0 else 'N/A'}
{weather_kenai[1] if len(weather_kenai) > 1 else 'N/A'}
{weather_kenai[2] if len(weather_kenai) > 2 else 'N/A'}
{weather_kenai[3] if len(weather_kenai) > 3 else 'N/A'}

----------------------------------------------------------------------------------------------
Anchorage 
Last update: {last_update_anchorage}

{weather_anchorage[0] if len(weather_anchorage) > 0 else 'N/A'}
{weather_anchorage[1] if len(weather_anchorage) > 1 else 'N/A'}
{weather_anchorage[2] if len(weather_anchorage) > 2 else 'N/A'}
{weather_anchorage[3] if len(weather_anchorage) > 3 else 'N/A'}

___________________________________________
Coastal Waters Forecast
National Weather Service Anchorage Alaska
{datetime.now().strftime('%I:%M %p %A %B %d %Y')}
{coastal_waters_forecast}
_________________________________________________________________________________________

Seldovia District Tides:
High Tide: {seldovia_tides[1] if len(seldovia_tides) > 1 else 'N/A'}
Low Tide: {seldovia_tides[0] if len(seldovia_tides) > 0 else 'N/A'}

Seward District Tides:
High Tide: {seward_tides[1] if len(seward_tides) > 1 else 'N/A'}
Low Tide: {seward_tides[0] if len(seward_tides) > 0 else 'N/A'}

Homer Sunrise/Sunset
Sunrise: {sunrise_homer}
Sunset: {sunset_homer}

Seward Sunrise/Sunset
Sunrise: {sunrise_seward}
Sunset: {sunset_seward}
"""
    return report

def main():
    report = format_weather_report()
    with open('weather.txt', 'w') as file:
        file.write(report)
    print("Report generated and written to weather.txt")

if __name__ == "__main__":
    main()
