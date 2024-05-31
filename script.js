async function fetchWeatherData() {
    const response = await fetch('weather.txt');
    const weatherData = await response.text();
    document.getElementById('weather').innerText = weatherData;
}

fetchWeatherData();
