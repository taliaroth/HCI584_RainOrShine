from flask import Flask, render_template
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

"""" TO DO: finish creating route for base.html to link to -
@app.route('/forecast', methods=['POST'])
def forecast():
    city = request.form.get('city')
    lat, long = get_cord(city)
"""

if __name__ == '__main__':
    # run on the local ip at the port number
    app.run(debug=True,port=5001)
