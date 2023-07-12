from datetime import datetime

import requests
from flask import Flask, render_template, request
from opencage.geocoder import OpenCageGeocode

# set flask app variable
app = Flask(__name__)

# read geocode api key from text file
with open('api_key.txt', 'r') as file:
    api_key = file.read().strip()
# read autocomplete api key
with open('api_auto_complete.txt', 'r') as file:
    api_key_auto = file.read().strip()


# import geocoder for weather
geocoder = OpenCageGeocode(api_key)
url = 'https://api.open-meteo.com/v1/forecast'


# route flask app to default base.html as homepage
# TO DO: Add zipcode or if location allowed auto locate
@app.route('/')
def home():
    return render_template('base.html')

@app.route('/autocomplete_geocode', methods=['GET'])
def autocomplete():
    #get current user input
    text = request.args.get('text')

    # set up url
    url = "https://api.geoapify.com/v1/geocode/autocomplete"

    # add api key
    params = {
        "text": text,
        "apiKey": api_key_auto
    }
    # create header
    headers = {
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()['features']

        #TO DO: add an error message if city not found - error handling

# add day and am/pm
# forecast flask route
@app.route('/forecast', methods=['POST'])
def forecast():

    # get user text from flask form
    city = request.form.get('city')

    # get cords using city name and geocoder
    lat, long = get_cord(city)
    if lat and long: # if both exist keep going
        json_data = get_forecast_daily(lat, long, 10)
        data = []

        # for each day create a row which will go to the html to read
        for i in range(len(json_data['daily']['time'])):

            # use precipitation to check if it's going to rain and then use image
            if json_data['daily']['precipitation_probability_mean'][i] > 0:
                image = 'rain.png'
            else:
                image = 'sun.png'

            # get the date and day of the week
            date_str = json_data['daily']['time'][i]
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')  # change the format here
            day_of_week = date_obj.strftime('%A')

            # create row using response json data
            row = [
                date_str,  # get time
                day_of_week,  # get day of the week
                json_data['daily']['temperature_2m_max'][i],  # get temp max for day - TODO: Get max and min
                json_data['daily']['precipitation_probability_mean'][i],  # get rain chances
                image
            ]

            # add day
            data.append(row)

        # return the html page with the data we want to pass in, and also pass in city name
        return render_template('forecast.html', city=city, data=data)


def get_forecast_daily(lat, long, forecast_d):  # creating an api call for user's input
    params = {
        'latitude': lat,
        'longitude': long,  # have to convert city to lat,long
        'forecast_days': forecast_d,  # number of days in forecast
        'temperature_unit': 'fahrenheit',  # Change unit maybe later according to user pref
        'precipitation_unit': 'mm',
        'windspeed_unit': 'kmh',
        'daily': 'temperature_2m_max,precipitation_probability_mean',
        'timezone': 'America/New_York',  # Change according to your timezone - later user could maybe do this
    }
    response = requests.get(url, params=params)
    return response.json()


def get_cord(city):

    # use geocoder and city name to find lat and lng
    response = geocoder.geocode(city)
    if response:
        if len(response):  # check if there is a response

            # read and return response
            return response[0]['geometry']['lat'], response[0]['geometry']['lng']
    else:
        print('city is not found')
        return None, None


def get_forecast_hourly(lat, long, forecast_d=1):  # creating an api call for user's (use one day)

    # city input for each hour
    params = {
        'latitude': lat,
        'longitude': long,
        'forecast_days': forecast_d,
        'temperature_unit': 'fahrenheit',
        'precipitation_unit': 'mm',
        'windspeed_unit': 'kmh',
        'hourly': 'temperature_2m,precipitation',
        'timezone': 'America/New_York',
    }
    response = requests.get(url, params=params)
    return response.json()

# add next 24 hours and day,am/pm
@app.route('/hourly_forecast', methods=['POST'])
def hourly_forecast():

    # get user input
    city = request.form.get('city')

    # get lat and long
    lat, long = get_cord(city)
    if lat and long:
        json_data = get_forecast_hourly(lat, long,2) # use 2 days now to get next 24 hours

        # create data needed for forecast
        data = []

        # use current time to only get hourly from now
        current_time = datetime.now()

        # parse data
        for i in range(len(json_data['hourly']['time'])):

            # get time we should filter for
            forecast_time = datetime.strptime(json_data['hourly']['time'][i], '%Y-%m-%dT%H:%M')

            if forecast_time >= current_time:
                if json_data['hourly']['precipitation'][i] > 0:
                    image = 'rain.png'
                else:
                    image = 'sun.png'

                # get day and get am/pm
                time_am_pm = forecast_time.strftime('%I:%M %p')
                day_str = forecast_time.strftime('%A')
                row = [
                    time_am_pm,
                    day_str,
                    json_data['hourly']['temperature_2m'][i],
                    json_data['hourly']['precipitation'][i],
                    image
                ]

                # add in data
                data.append(row)

                # break loop after 24 hours
                if len(data) >= 24:
                    break

                # render correct template and pass data to html
        return render_template('hourly_forecast.html', city=city, data=data)


if __name__ == '__main__':

    # run on the local ip at the port number
    app.run(debug=True, port=5001)

