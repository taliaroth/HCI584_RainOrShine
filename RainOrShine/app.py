import requests
from flask import Flask, render_template, request
from opencage.geocoder import OpenCageGeocode

# set flask app variable
app = Flask(__name__)


# read api key from text file
with open('api_key.txt', 'r') as file:
    api_key = file.read().strip()

# import geocoder for weather
geocoder = OpenCageGeocode(api_key)
url = 'https://api.open-meteo.com/v1/forecast'

# route flask app to default base.html as homepage
@app.route('/')
def home():
    return render_template('base.html')

#forecast flask route
@app.route('/forecast', methods=['POST'])
def forecast():
    # get user text from flask form
    city = request.form.get('city')

    # get cords using city name and geocoder
    lat, long = get_cord(city)
    # if both exist keep going
    if lat and long:
        json_data = get_forecast_daily(lat, long, 10)
        data = []
        # for each day create a row which will go to the html to read
        for i in range(len(json_data['daily']['time'])):
            # use precipitation to check if it's going to rain and then use image
            if json_data['daily']['precipitation_probability_mean'][i] > 0:
                image = 'rain.png'
            else:
                image = 'sun.png'
            # create row using response json data
            row = [
                json_data['daily']['time'][i],  # get time
                json_data['daily']['temperature_2m_max'][i], #get temp max for day - TODO: Get max and min
                json_data['daily']['precipitation_probability_mean'][i], # get rain chances
                image
            ]
            # add day
            data.append(row)
        # return the html page with the data we want to pass in, and also pass in city name
        return render_template('forecast.html', city=city, data=data)


def get_forecast_daily(lat, long, forecast_d): #creating an api call for user's input
    params = {
        'latitude': lat,
        'longitude': long, #have to convert city to lat,long
        'forecast_days': forecast_d, #number of days in forecast
        'temperature_unit': 'fahrenheit', # Change unit maybe later according to user pref
        'precipitation_unit': 'mm',
        'windspeed_unit': 'kmh',
        'daily': 'temperature_2m_max,precipitation_probability_mean',
        'timezone': 'America/New_York',  # Change according to your timezone - later user could maybe do this
    }
    response = requests.get(url, params=params)
    return response.json()

def get_cord(city):
    #use geocoder and city name to find lat and lng
    response =  geocoder.geocode(city)
    if  response:
        if len(response): #check if there is a response
            # read and return response
            return response[0]['geometry']['lat'], response[0]['geometry']['lng']
    else:
        print('city is not found')
        return None, None


if __name__ == '__main__':
    # run on the local ip at the port number
    app.run(debug=True,port=5001)
