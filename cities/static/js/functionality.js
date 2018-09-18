// learn more links


var forecast = false;
// forecast
function showForecast() {
    forecast = !forecast;
    document.getElementById('weather').style.display = forecast ? 'block' : 'none';
    var not_weather = document.getElementsByClassName('not-weather');
    for (var i = 0; i < not_weather.length; i++) {
        not_weather[i].style.display = forecast ? 'none' : 'block';
    }
    document.getElementById('showForecast').innerHTML = forecast ? 'Hide' : 'Show';
}
