# fastAPI_weather_api
download source code 
go to folder
open cmd
1.run these commands one by one
pip install python-weather
pip install requests

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd api
uvicorn main:app --reload
Then
write localhost:8000/docs in browser
now 
you can register a user 
or
you can login with this username and password
username : jaffar
password : password
after execute
copy access token from response 
put access token in autorize
then 
go to weather api and add city name 
you can see temperature and description of city
