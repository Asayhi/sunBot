#   SunBot v0.1.2
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT
#   WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
#   INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
#   OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
#   PURPOSE AND NONINFRINGEMENT. IN NO EVENT 
#   SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE 
#   LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
#   TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
#   CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
#   DEALINGS IN THE SOFTWARE. 

import tweepy
import logging
import astral
from astral.sun import sun
import datetime
import time
import configparser
import pytz
import wetterbericht as wetter


logger = logging.getLogger()


def create_api():
    config = configparser.ConfigParser()
    config.read("Twitter_keys.cfg")
    
    consumer_key = config['KEYS']['apiKey']
    consumer_secret = config['KEYS']['apiSecretKey']
    access_token = config['TOKEN']['accessToken']
    access_token_secret = config['TOKEN']['accessTokenSecret']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    print("API created")

    return api

def auth_api(api):
    try:
        api.verify_credentials()
        print("Authentication:\tOK")
        return True
    except Exception as e:
        print("Authentication:\tError authorizing API")
        print("Authentication:\tException occured: " + e)
        return False

def get_sun_event(today):
    config = configparser.ConfigParser()
    config.read("Twitter_keys.cfg")
    lat = config['Astral']['lat']
    lon = config['Astral']['lon']

    year = today.year
    month = today.month
    day = today.day
    home = astral.LocationInfo('MyHome', 'Bavaria', 'Europe/Berlin', lat, lon)
    s = sun(home.observer, date=datetime.date(year, month, day), tzinfo=home.timezone)
    sunrise = s['sunrise']
    sunset = s['sunset']

    return sunrise, sunset


def create_tweet(time, event):
    stringTime = time.strftime("%H:%M")
    defaultString = "SunBot praising the sun\nEs ist " + stringTime + " Uhr\n"
    if event == "sunrise":
        eventString = "Die Sonne ist aufgegangen\n"

    else:
        eventString = "Die Sonne geht unter\n"

    weatherString = wetter.allInOneWeatherMsg()
    endString = "Lobet die Sonne\n#PraiseTheSun #Sonnengruss\n"
    emoji = u"\U0001F31E"
    sunTweet = emoji + emoji + "\n" + defaultString + eventString + "\n"+ weatherString + endString + emoji + emoji
    
    return sunTweet

def post_tweet(api, content):
    try:
        api.update_status(content)
    except Exception as e:
        print("Error while tweeting")
        raise e
    


def wait_until(end_datetime):
    while True:
        now = datetime.datetime.now()
        
        cet = pytz.timezone('Europe/Amsterdam')
        now_aware = cet.localize(now)
        diff = (end_datetime - now_aware).total_seconds()
        if diff < 0: return       # In case end_datetime was in past to begin with
        time.sleep(diff/2)
        if diff <= 0.1: return


def main():

    api = create_api()
    today = datetime.datetime.today()
    sunrise, sunset = get_sun_event(today)
    cet = pytz.timezone('Europe/Amsterdam')
    now = datetime.datetime.now()
    print("Loop at: \t" + now.strftime('%Y-%m-%d %H:%M:%S'))


    while True:
        now = datetime.datetime.now()
        now_aware = cet.localize(now)
        tommorow = now_aware + datetime.timedelta(days=1)
        
        if sunrise > now_aware:
            auth_is_ok = auth_api(api)
            if not auth_is_ok:
                api = create_api()
                auth_is_ok = auth_api(api)

            print("Waiting till: \t" + sunrise.strftime('%H:%M:%S'))
            wait_until(sunrise)
            rise_tweet = create_tweet(sunrise, "sunrise")
            print("Tweeting:\n"+ rise_tweet + "\nTime: " + sunrise.strftime('%Y-%m-%d %H:%M:%S'))
            post_tweet(api, rise_tweet)

        now = datetime.datetime.now()
        now_aware = cet.localize(now)
        if sunset > now_aware:
            auth_is_ok = auth_api(api)
            if not auth_is_ok:
                api = create_api()
                auth_is_ok = auth_api(api)

            print("Waiting till: \t" + sunset.strftime('%H:%M:%S'))
            wait_until(sunset)
            set_tweet = create_tweet(sunset, "sunset")
            print("Tweeting:\n"+ set_tweet + "\nTime: " + sunset.strftime('%Y-%m-%d %H:%M:%S'))
            post_tweet(api, set_tweet)

        sunrise, sunset = get_sun_event(tommorow)
        time.sleep(10)
        now = datetime.datetime.now()
        print("End of Loop at:\t" + now.strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == __name__:
    main()
