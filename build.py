import datetime
import os
import sys
from pathlib import Path
from shutil import copy2, rmtree
from typing import Any

from cloudflare import Cloudflare
from jinja2 import Environment, FileSystemLoader

from src.data import FALLBACK_PALETTES, MOCK_EVENTS, TAG_DEFINITIONS

DEPS = Path(__file__).parent / "modules"
TARGET = Path(__file__).parent / "dist"
TEMPLATES = Path(__file__).parent / "templates"


def build_dist(events: list[dict[str, Any]], tags: dict[str, dict]):

    if TARGET.exists():
        rmtree(TARGET)
    TARGET.mkdir()

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("index.jinja")
    rendered_output = template.render(
        {
            "events": events,
            "tags": tags,
            "build_date": datetime.datetime.now().isoformat(),
        }
    )
    (TARGET / "index.html").write_text(rendered_output)

    copy2(DEPS / "index.global.js", TARGET / "index.global.js")
    copy2(TEMPLATES / "styles.css", TARGET / "styles.css")


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

ALL_EVENTS = """
    SELECT Name from tags
"""


def fetch_events_from_d1(
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
                class_names = item["matched_tags"].split(",")
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


def fetch_tags_from_d1(
    account_id: str, database_id: str, api_token: str
) -> list[dict[str, Any]]:
    client = Cloudflare(api_token=api_token)
    response = client.d1.database.query(
        account_id=account_id,
        database_id=database_id,
        sql=ALL_EVENTS,
    )

    # Extract results
    if response.success:
        tag_list = []
        raw_res = response.result[0].results
        if raw_res:
            for item in raw_res:
                tag_list.append(item["name"])
            return tag_list
    raise Exception("Query failed:", response.errors)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "local":
        events = MOCK_EVENTS
        tags = set()
        for one_event in events:
            for one_tag in one_event["classNames"]:
                tags.add(one_tag)
    else:
        account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
        api_token = os.getenv("CLOUDFLARE_API_TOKEN", "")
        database_id = os.getenv("CLOUDFLARE_DATABASE_ID", "")
        events = fetch_events_from_d1(account_id, database_id, api_token)
        tags = fetch_tags_from_d1(account_id, database_id, api_token)

    tag_definitions = TAG_DEFINITIONS.copy()
    last_fallback = 0
    for one_tag in tags:
        if one_tag not in tag_definitions:
            last_fallback += 1
            tag_definitions[one_tag] = FALLBACK_PALETTES[
                last_fallback % len(FALLBACK_PALETTES)
            ]

    build_dist(events, tag_definitions)
