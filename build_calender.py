import json
import boto3
import httpx
from datetime import datetime, timedelta, UTC
from jinja2 import Template
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    google_api_key: str
    calendar_id: str
    r2_account_id: str
    r2_access_key_id: str
    r2_secret_access_key: str
    r2_bucket_name: str
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

def fetch_and_build():
    # 1. Calculate time windows (pulling data from 1 month ago up to 6 months out)
    now = datetime.now(tz=UTC)
    start_time = (now).isoformat() + "Z"
    end_time = (now + timedelta(days=180)).isoformat() + "Z"

    google_url = (
        f"https://googleapis.com{settings.calendar_id}/events"
        f"?key={settings.google_api_key}"
        f"&timeMin={start_time}"
        f"&timeMax={end_time}"
        f"&singleEvents=true"
    )

    # 2. Fetch raw events
    response = httpx.get(google_url)
    if response.status_code != 200:
        print(f"Error fetching Google Calendar: {response.text}")
        return

    data = response.json()
    safe_events = []

    # 3. Clean all origin tracing metadata completely
    for event in data.get("items", []):
        start_data = event.get("start", {})
        end_data = event.get("end", {})
        
        safe_events.append({
            "title": event.get("summary", "Busy"),
            "start": start_data.get("dateTime") or start_data.get("date"),
            "end": end_data.get("dateTime") or end_data.get("date"),
            "allDay": "dateTime" not in start_data
        })

    # 4. Render the safe events into the template
    with open("template.html", "r") as file:
        template_content = file.read()

    template = Template(template_content)
    rendered_html = template.render(events_json=json.dumps(safe_events))


    print("Success: Secure static calendar published to R2 bucket.")

if __name__ == "__main__":
    fetch_and_build()
