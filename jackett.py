import os
import requests
from dotenv import load_dotenv

load_dotenv()

def search(query, tracker):

    url = 'http://192.168.1.154:9117/api/v2.0/indexers/all/results'
    
    params = {
        "apikey": os.getenv("JACKETT_API_KEY"),
        "Query": query
    }

    if tracker != 'All':
        params["Tracker[]"] = tracker
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("Results", [])
    else:
        print(f"Error: {response.status_code}, {response.text}")


def getTrackers():
    url = f'http://192.168.1.154:9117/api/v2.0/indexers/tag:added/results'
    response = requests.get(url, params = {
        "apikey": os.getenv("JACKETT_API_KEY"),
    })

    if response.status_code == 200:
        data = response.json()
        return data.get("Indexers", [])
    else:
        print(f"Error: {response.status_code}, {response.text}")

