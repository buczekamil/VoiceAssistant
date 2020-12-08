import os
import webbrowser
import speech_recognition as sr
import pyttsx3 as tts
import requests
from datetime import date, datetime
from beepy import beep
import api

r = sr.Recognizer()
r.energy_threshold = 200


def getText():
    with sr.Microphone() as source:
        try:
            audio = r.listen(source)
            text = r.recognize_google(audio, language='pl-PL')
            if text != "":
                return text
            return 0
        except:
            return 0


def getDemand():
    with sr.Microphone() as source:
        beep(sound=1)
        try:
            audio = r.listen(source, timeout=10)
            text = r.recognize_google(audio, language='pl-PL')
            if text != "":
                return text
            return 0
        except:
            return 0


def getUpdate():
    url_warsaw = f"http://api.openweathermap.org/data/2.5/weather?q=Warsaw&units=metric&appid={api.weather_api}"
    city = "Warsaw"
    Warsaw_weather = requests.get(
        url_warsaw.format(city)).json()
    weather = {
        'city': city,
        'temperature': Warsaw_weather['main']['temp'],
        'description': Warsaw_weather['weather'][0]['description'],
        'pressure': Warsaw_weather['main']['pressure'],
        'temperature_min': Warsaw_weather['main']['temp_min'],
        'temperature_max': Warsaw_weather['main']['temp_max'],
        'temperature_feels_like': Warsaw_weather['main']['feels_like'],
        'sunrise': Warsaw_weather['sys']['sunrise'],
        'sunset': Warsaw_weather['sys']['sunset'],

    }
    weather_descriptions = {
        'clear sky': 'bezchmurne niebo',
        'few clouds': 'lekkie zachmurzenie',
        'scattered clouds': 'zachmurzenie',
        'broken clouds': 'duże zachmurzenie',
        'shower rain': 'prognozowany opad deszczu',
        'rain': 'prognozowany mocny opad deszczu',
        'thunderstrom': 'pronozowane burze',
        'snow': 'prognozowany opad śniegu',
        'mist': 'możliwa mgła'
    }
    celcius = round(weather['temperature'])
    engine = tts.init()
    engine.setProperty('rate', 215)
    today = date.today()
    date_today = today.strftime("%d/%m/%Y")
    engine.say(f"Dzisiaj mamy {date_today}")
    sunrise = datetime.fromtimestamp(weather['sunrise'])
    sunset = datetime.fromtimestamp(weather['sunset'])
    engine.say(f"Wschód słońca: {sunrise.hour}:{sunrise.minute}")
    engine.say(f"Zachód słońca: {sunset.hour}:{sunset.minute}")
    if celcius == -1 or celcius == 1:
        engine.say(f"W Warszawie jest {celcius} stopień celcjusza,")
    elif celcius < -1 and celcius >= -4 or celcius > 1 and celcius <= 4:
        engine.say(f"W Warszawie są {celcius} stopnie celcjusza, ")
    else:
        engine.say(f"W Warszawie jest {celcius} stopni celcjusza,")
    engine.say(
        f"temperatura minimalna: {round(weather['temperature_min'])}, temperatura maksymalna: {round(weather['temperature_max'])}"
        f"temperatura odczuwalna: {round(weather['temperature_feels_like'])}, ciśnienie: {round(weather['pressure'])} hektopaskali"
    )
    engine.say(f"{weather_descriptions[weather['description']]}")
    engine.runAndWait()
    engine.stop()


while True:
    txt = getText()
    engine = tts.init()
    engine.setProperty('rate', 200)
    if not txt == 0:
        if txt in ['ola', "Ola", "Hej", "Hey", "hej", "hey", "włącz"]:
            txt = getDemand()
            print(txt)
            try:
                if txt.lower() in ["kampus", 'włącz kampus']:
                    engine.say("Włączam radio kampus")
                    webbrowser.open('https://stream.radiokampus.fm/kampus')
                elif txt.lower() in ["dzisiaj", "info", "pogoda"]:
                    getUpdate()
                elif txt.lower() in ['lofi', "włącz lofi"]:
                    engine.say("Włączam radio lofi")
                    engine.runAndWait()
                    engine.stop()
                    webbrowser.open('https://www.youtube.com/watch?v=7NOSDKb0HlU&feature=youtu.be')
                elif txt.lower() in ['spotify', 'włącz spotify']:
                    engine.say("włączam spotifaj")
                    engine.runAndWait()
                    engine.stop()
                    command = r"/Applications/Spotify.app/Contents/MacOS/Spotify"
                    os.system(command)
                continue
            except AttributeError:
                print("Nie udało się rozpoznać...")
                engine.say("Nie rozumiem")
                engine.runAndWait()
                engine.stop()
                continue
