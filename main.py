import requests
from datetime import datetime
from redmail import outlook
import time


MY_LAT = 0.0000 # Your latitude
MY_LONG = 0.0000 # Your longitude

outlook.username = "your email"
outlook.password = "your password"

def send_email():
    outlook.send(
        receivers=["your email"],
        subject="International Space Station above you.",
        text="It is dark outside and the ISS is above your coordinates."
    )

def iss_location():
    '''Checks for ISS location'''
    
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    print(f'{iss_latitude}, {iss_longitude}')

    
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True
    else:
        return False

def daylight_check():
    '''Checks to see if it is daylight or dark'''

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour

    if sunset <= time_now or time_now <= sunrise:
        return True
    else:
        return False
    
while True: #Checks once per minute
    daylight_check()
    iss_location()
    if daylight_check()==True and iss_location()==True:
        send_email()
    else:
        time.sleep(60)
        



