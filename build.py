import datetime
import os
import sys
from pathlib import Path
from shutil import copy2, rmtree
from typing import Any

from cloudflare import Cloudflare
from jinja2 import Environment, FileSystemLoader

DEPS = Path(__file__).parent / "modules"
TARGET = Path(__file__).parent / "dist"
TEMPLATES = Path(__file__).parent / "templates"


def build_dist(events: list[dict[str, Any]]):

    if TARGET.exists():
        rmtree(TARGET)
    TARGET.mkdir()

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("index.jinja")
    rendered_output = template.render({"events": events})
    (TARGET / "index.html").write_text(rendered_output)

    copy2(DEPS / "index.global.js", TARGET / "index.global.js")
    copy2(TEMPLATES / "styles.css", TARGET / "styles.css")


MOCK_EVENTS = [
    {
        "title": "All Day Event",
        "start": "2026-06-01",
        "classNames": ["class-all", "class-medical", "class-personal"],
        "link": "https://www.marcelldls.lol/0",
    },
    {
        "title": "Long Event",
        "start": "2026-06-07",
        "end": "2026-06-10",
        "classNames": ["class-all", "class-test"],
        "link": "https://www.marcelldls.lol/0",
    },
    {
        "title": "Repeating Event",
        "start": "2026-06-09T16:00:00",
        "classNames": ["class-all"],
        "link": "https://www.marcelldls.lol/0",
    },
    {
        "title": "Repeating Event",
        "start": "2026-06-16T16:00:00",
        "classNames": ["class-all"],
        "link": "https://www.marcelldls.lol/0",
    },
    {
        "title": "Conference",
        "start": "2026-06-11",
        "end": "2026-06-13",
        "classNames": ["class-all", "class-business", "class-personal"],
        "link": "https://www.marcelldls.lol/0",
    },
    {
        "title": "Meeting",
        "start": "2026-06-12T10:30:00",
        "end": "2026-06-12T12:30:00",
        "classNames": ["class-all"],
        "link": "https://www.marcelldls.lol/0",
    },
    {
        "title": "Lunch",
        "start": "2026-06-12T12:00:00",
        "classNames": ["class-all"],
        "link": "https://www.marcelldls.lol/0",
    },
    {
        "title": "Meeting",
        "start": "2026-06-12T14:30:00",
        "classNames": ["class-all"],
        "link": "https://www.marcelldls.lol/0",
    },
    {
        "title": "Birthday Party",
        "start": "2026-06-13T07:00:00",
        "classNames": ["class-all"],
        "link": "https://www.marcelldls.lol/0",
    },
    {
        "title": "Click for Google",
        "start": "2026-06-28",
        "classNames": ["class-all"],
        "link": "https://www.marcelldls.lol/0",
    },
    {
        "title": "Dentist Checkup",
        "start": "2026-06-25T10:00:00",
        "end": "2026-06-25T11:30:00",
        "classNames": ["class-all", "class-medical"],
        "link": "https://www.marcelldls.lol/0",
    },
    {
        "title": "Quarterly Board Meeting",
        "start": "2026-06-27T14:00:00",
        "end": "2026-06-27T16:00:00",
        "classNames": ["class-all", "class-business"],
        "link": "https://www.marcelldls.lol/0",
    },
    {
        "title": "Dinner with Parents",
        "start": "2026-06-29T19:00:00",
        "classNames": ["class-all", "class-personal", "class-medical"],
        "link": "https://www.marcelldls.lol/0",
    },
]

TAGGED_EVENTS = """
    WITH filtered_events AS (
        SELECT id, start_datetime, end_datetime, name
        FROM events
        WHERE start_datetime > ?
    )
    SELECT
        fe.id,
        fe.start_datetime,
        fe.end_datetime,
        fe.name,
        GROUP_CONCAT(et.tag_name, ',') AS matched_tags
    FROM filtered_events fe
    JOIN events_tags et
        ON et.event_id = fe.id
    GROUP BY fe.id
"""


def fetch_from_d1(
    account_id: str, database_id: str, api_token: str
) -> list[dict[str, Any]]:
    client = Cloudflare(api_token=api_token)
    response = client.d1.database.query(
        account_id=account_id,
        database_id=database_id,
        sql=TAGGED_EVENTS,
        params=["1"],  # TODO: filter past events by date
    )

    # Extract results
    if response.success:
        res_list = []
        raw_res = response.result[0].results
        if raw_res:
            for item in raw_res:
                class_names = [
                    f"class-{one_tag}" for one_tag in item["matched_tags"].split(",")
                ]
                end_datetime = datetime.datetime.fromtimestamp(
                    item["end_datetime"], tz=datetime.timezone.utc
                )
                start_datetime = datetime.datetime.fromtimestamp(
                    item["start_datetime"], tz=datetime.timezone.utc
                )
                res_list.append(
                    {
                        "end": end_datetime.isoformat(),
                        "start": start_datetime.isoformat(),
                        "title": item["name"],
                        "classNames": class_names,
                        "link": "https://www.marcelldls.lol/0",
                    }
                )
            return res_list
    raise Exception("Query failed:", response.errors)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "local":
        events = MOCK_EVENTS
    else:
        account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
        api_token = os.getenv("CLOUDFLARE_API_TOKEN", "")
        database_id = os.getenv("CLOUDFLARE_DATABASE_ID", "")
        events = fetch_from_d1(account_id, database_id, api_token)
    build_dist(events)
