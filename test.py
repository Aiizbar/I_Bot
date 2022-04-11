import requests


def weather(update):
    geocoder_uri = geocoder_request_template = "http://geocode-maps.yandex.ru/1.x/"
    response = requests.get(geocoder_uri, params={
        "apikey": "8f291e24-fa66-4c82-81c9-cbf8e4a87a66",
        "format": "json",
        "geocode": update
    })

    toponym = response.json()["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    # print(((toponym['Point']['pos']).split(' '))[0])
    ll, spn = ((toponym['Point']['pos']).split(' '))[0], ((toponym['Point']['pos']).split(' '))[1]
    print(ll, spn)

    weather_api_reqest = \
        f'https://api.openweathermap.org/data/2.5/weather?lat={ll}&lon={spn}&appid=86269be3456b3b7a2752803a0eefcd22'
    weather_reqest = requests.get(weather_api_reqest)
    WeatherNow = weather_reqest.json()
    answer = (f'temperature in degrees Celsius: {int(WeatherNow["main"]["temp"]) - 273}' + '\n'
              + f'wind speed: {WeatherNow["wind"]["speed"]} м/с' + '\n'
              + f'main: {WeatherNow["weather"][0]["description"]}')
    return answer


print(weather('Шадринск'))

