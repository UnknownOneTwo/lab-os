import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

# === CONFIG ===
GRAFANA_URL = "http://192.168.10.102:3000"
GRAFANA_TOKEN = os.getenv("GRAFANA_API_KEY")
HEADERS = {
    "Authorization": f"Bearer {GRAFANA_TOKEN}",
    "Content-Type": "application/json"
}

# === REQUEST DATA SOURCES ===
try:
    response = requests.get(f"{GRAFANA_URL}/api/datasources", headers=HEADERS)
    response.raise_for_status()
    datasources = response.json()

    print("\n📋 Available Datasources in Grafana:")
    for ds in datasources:
        print(f"- Name: {ds['name']} | Type: {ds['type']} | UID: {ds.get('uid', '?')}")

except Exception as e:
    print(f"❌ Failed to fetch datasources: {e}")
