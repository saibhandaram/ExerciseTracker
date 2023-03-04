import requests
from datetime import datetime
import os

# GENDER = YOUR GENDER
# WEIGHT_KG = YOUR WEIGHT
# HEIGHT_CM = YOUR HEIGHT
# AGE = YOUR AGE

APP_ID = os.environ['APP_ID']
API_KEY = os.environ['API_KEY']
exercise_endpoint = os.environ['exercise_endpoint']
sheet_endpoint = os.environ['sheet_endpoint']
TOKEN = os.environ['TOKEN']
sheet_header = {"Authorization": TOKEN}


exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    # "gender": GENDER,
    # "weight_kg": WEIGHT_KG,
    # "height_cm": HEIGHT_CM,
    # "age": AGE
}

response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()

################### Start of Step 4 Solution ######################

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, headers=sheet_header)
    sheet_response.raise_for_status()

print(sheet_response.text)
