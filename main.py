import os
import webbrowser
import speech_recognition as sr
import pyttsx3 as tts
import pyaudio
import requests
from datetime import date

r = sr.Recognizer()
engine = tts.init()
engine.setProperty('rate', 170)


def getText():
    with sr.Microphone() as source:
        try:
            print("Słucham...")
            engine = tts.init()
            engine.setProperty('rate', 200)
            engine.say("Słucham")
            engine.runAndWait()
            engine.stop()
            audio = r.listen(source)
            text = r.recognize_google(audio, language='pl-PL')
            if text != "":
                return text
            return 0
        except:
            return 0


import api


def getWeather():
    url_warsaw = f'http://api.openweathermap.org/data/2.5/weather?q=Warsaw&units=metric&appid={api.weather_api}'
    city = "Warsaw"
    Warsaw_weather = requests.get(
        url_warsaw.format(city)).json()
    weather = {
        'city': city,
        'temperature': Warsaw_weather['main']['temp'],
        'description': Warsaw_weather['weather'][0]['description'],
    }
    weather_descriptions = {
        'clear sky': 'brak zachmurzenia',
        'few clouds': 'lekkie zachmurzenie',
        'scattered clouds': 'zachmurzenie',
        'broken clouds': 'duże zachmurzenie',
        'shower rain': 'obecnie pada deszcz',
        'rain': 'obecnie pada dość mocno',
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
    engine.say(f"{weather_descriptions[weather['description']]}")
    if celcius == -1 or celcius == 1:
        engine.say(f"W Warszawie jest {celcius} stopień celcjusza w Warszawie")
        engine.runAndWait()
        engine.stop()
    elif celcius < -1 and celcius >= -4 or celcius > 1 and celcius <= 4:
        engine.say(f"W Warszawie są {celcius} stopnie celcjusza ")
        engine.runAndWait()
        engine.stop()
    else:
        engine.say(f"W Warszawie jest {celcius} stopni celcjusza")
        engine.runAndWait()
        engine.stop()


while True:
    txt = getText()
    engine = tts.init()
    engine.setProperty('rate', 200)
    if not txt == 0:
        print(txt)
        if txt.lower() == "włącz radio kampus":
            engine.say("Włączam radio kampus")
            engine.runAndWait()
            engine.stop()
            webbrowser.open('https://stream.radiokampus.fm/kampus')
        elif txt.lower() == 'pogoda' or txt.lower() == "jaka jest pogoda":
            getWeather()
        elif txt.lower() == "włącz lofi" or "lofi":
            engine.say("Włączam radio lofi")
            engine.runAndWait()
            engine.stop()
            webbrowser.open('https://www.youtube.com/watch?v=7NOSDKb0HlU&feature=youtu.be')
        elif txt.lower() == "włącz spotify":
            engine.say("włączam spotifaj")
            engine.runAndWait()
            engine.stop()
            command = r"/Applications/Spotify.app/Contents/MacOS/Spotify"
            os.system(command)

        break
    else:
        print("Nie udało się rozpoznać...")
        engine.setProperty('rate', 200)
        engine.say("Nie rozumiem, powtórz")
        engine.runAndWait()
        engine.stop()
        continue
