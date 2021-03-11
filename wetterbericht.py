# wetterbericht V0.0.1

import configparser
from pyowm.owm import OWM


def clear():
    emoji = u"\u2600"
    return emoji

def few_clouds():
    emoji = u"\U0001F324"
    return emoji

def clouds():
    emoji = u"\u2601"
    return emoji

def rain():
    emoji = u"\U0001f327"
    return emoji

def thunder():
    emoji = u"\U0001f329"
    return emoji

def snow():
    emoji = u"\U0001f32b"
    return emoji

def mist():
    emoji = u"\u2744"
    return emoji



def createOwmManager():
    '''
    Function that creates and returns am OWM Manager Object.
    It reads the specified api keys from a given cfg file

    Parameters:
        None

    Returns:
        weather_manager: a owm weather_manager object
    '''
    config = configparser.ConfigParser()
    config.read("Twitter_keys.cfg")
    api_key = config['OWMKEY']['weatherKey']
    owm = OWM(api_key)
    weather_manager = owm.weather_manager()

    return weather_manager

def callWeather(weather_manager):
    '''
    Returns the current weather as a short status description aswell as
    a dictionary of temperatures

    Parameters:
        weather_manager: a owm weather_manager object

    Returns:
        status: current status of the weather (e.g. "Clear", "Cloudy"...)
        temp_dict_celsius: a dictionary of temeratures in celsius
    '''
    config = configparser.ConfigParser()
    config.read("Twitter_keys.cfg")
    location = config['OWMLOC']['location']
    observation = weather_manager.weather_at_place(location)
    weather = observation.weather
    status = weather.status
    temp_dict_celsius = weather.temperature('celsius')
    return status, temp_dict_celsius

def getStatus(status):
    '''
    Returns the unicode representation of the corresponding weather
    emojis

    Parameters:
        status: string describing the current status of the weather
    
    Returns:
        current_weather:    string of the unicode representation of the
                            emoji
    '''
    if status == 'Thunderstorm':
        current_weather = thunder()
    if status == 'Drizzle' or status == 'Rain':
        current_weather = rain()
    if status == 'Snow':
        current_weather = snow()
    if status == 'Mist':
        current_weather = mist()
    if status == 'Clear':
        current_weather = clear()
    if status == 'Clouds':
        current_weather = clouds()
    elif current_weather == None:
        current_weather = False

    return current_weather

def createWeatherMsg(status, temp):

    weather_emoji = getStatus(status)
    if weather_emoji:
        weather_line = "Wetter: " + weather_emoji + "\n"
    else:
        weather_line = ""
    
    temperature_line = "Temperatur: " + str(temp['temp']) + " °C\n"

    return weather_line + temperature_line

def allInOneWeatherMsg():

    mgr = createOwmManager()
    status, temp = callWeather(mgr)
    msg = createWeatherMsg(status, temp)
    
    return msg


    
if __name__ == "__main__":
    mgr = createOwmManager()
    status, temp = callWeather(mgr)
    msg = createWeatherMsg(status, temp)

    print(msg)

