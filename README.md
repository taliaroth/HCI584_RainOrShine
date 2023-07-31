# RainOrShine_HCI584

General Description

This project is a web-based app that will give weather predictions. Users can use this app to help with travel plans and daily outings or stay informed on the weather.


The application is pulling from Open-Meteo’s API to gather past weather data. The user can search for their desired city and view the predicted weather for that place. This application will allow users to view weather predictions hourly or daily. The user will be able to see predictions for temperature and precipitation.

* Download the newest version of [Python 3](https://www.python.org/downloads/ "Python 3").
* Next, make sure you have Pip installed using this [guide ](https://pip.pypa.io/en/stable/installation/ "guide").
* Create an API key for the geocoding by going to OpenCage’s [website](https://opencagedata.com/ "website") and signing up.
* Create an API key for autocomplete by going to Geoapify [website](https://www.geoapify.com/ "website") and signing up.
* Once you have both API keys, place the OpenCage key in api_geocode.txt, then place the Geoapify in api_auto_complete.txt.
* Now you can start running the app in the terminal cd to the main project folder where app.py is. Use this [guide ](https://tutorials.codebar.io/command-line/introduction/tutorial.html "guide") if you are first starting with terminal commands.
* In your terminal, use the requirements.txt file by entering the command - pip install -r requirements.txt
* Here, use this command to tell Flask where the main part of your app is stored - export FLASK_APP=app
* Now use this command to start the app -  flask run
* You should see a hyperlink, click this, and it will take you to your app

