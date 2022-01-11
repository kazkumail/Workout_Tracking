import os
import requests
from datetime import datetime
APP_ID = os.environ.get("ENV_APP_ID")
API_KEY = os.environ.get("ENV_API_KEY")
AUTH_TOKEN = os.environ.get("ENV_AUTH_TOKEN")
GENDER = "male"
WEIGHT_KG = "77.1107"
HEIGHT_CM = "165"
AGE = "24"

Exercise_Endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEETY_ENDPOINT = os.environ.get("ENV_SHEETY_ENDPOINT")


headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

Exercise_text = input("What Exercise did you complete?: ")

Exercise_parameters = {
    "query": Exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(url=Exercise_Endpoint, json=Exercise_parameters, headers=headers)
result = response.json()

today_date = datetime.now().strftime("%m/%d/%Y")
now_time = datetime.now().strftime("%X")


for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise['name'].title(),
            "duration": exercise['duration_min'],
            "calories": exercise['nf_calories']
        }
    }

    bearer_headers = {
        "Authorization": f"Bearer {AUTH_TOKEN} "
    }

    sheet_response = requests.post(SHEETY_ENDPOINT, json=sheet_inputs, headers=bearer_headers)
    print(sheet_response.text)
