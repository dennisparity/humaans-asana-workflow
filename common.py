import os
from pprint import pprint

import requests

ASANA_TOKEN = TBC
ASANA_HEADERS = {
    "Authorization": f"Bearer {ASANA_TOKEN}"
}
ASANA_PREFETCH_TASKS = 1000
ASANA_LIST_PROJECT_TASKS_URL = f"https://app.asana.com/api/1.0/projects/%s/tasks"
ASANA_CREATE_TASK_URL = f"https://app.asana.com/api/1.0/tasks"
ASANA_UPDATE_TASK_URL = f"https://app.asana.com/api/1.0/tasks/%s"
ASANA_FIELD_URL = "1205125498486542"
ASANA_FIELD_POST_ID = "1205125504797456"
ASANA_FIELD_KSM = "1205123893904026"
ASANA_FIELD_DOT = "1205124081120645"
ASANA_FIELD_PROPOSER = "1205123896288332"
ASANA_FIELD_TRACK_NAME = "1205123984036116"
ASANA_FIELD_VOTES_RATIO = "1205124081629877"
ASANA_FIELD_TRACK_NAME_MAPPING = {
    0: "1205124076472919",  # Root
    1: "1205124076472924",  # Whitelisted Caller
    10: "1205124076472930",  # Staking Admin,
    11: "1205123984036117",  # Treasurer
    12: "1205124076472927",  # Lease Admin
    13: "1205124076472925",  # Fellowship Admin
    14: "1205124076472928",  # General Admin
    15: "1205124076472920",  # Auction Admin
    20: "1205124076472926",  # Referendum Canceller
    21: "1205124076472929",  # Referendum Killer
    30: "1205124076472921",  # Small Tipper
    31: "1205124076472923",  # Big Tipper
    32: "1205123984036118",  # Small Spender
    33: "1205123984036128",  # Medium Spender
    34: "1205123984036126",  # Big Spender
}
ASANA_FIELD_STATUS = "1205123984691610"
ASANA_FIELD_STATUS_MAPPING = {
    "Created": "1205454591294955",
    "DecisionDepositPlaced": "1205123984691611",
    "ConfirmStarted": "1205454591294956",
    "Confirmed": "1205454591294957",
    "Submitted": "1205123984691616",
    "Deciding": "1205123984691615",
    "TimedOut": "1205123984691614",
    "Executed": "1205123984691613",
    "Rejected": "1205123984691612",
}
ASANA_FIELD_TOPIC = "1205124038793931"
ASANA_FIELD_PROPOSED_AT = "1205124037532231"

POLKASSEMBLY_ALL_POST_LIST_URL = "https://api.polkassembly.io/api/v1/latest-activity/all-posts"
POLKASSEMBLY_ON_CHAIN_POST_LIST_URL = "https://api.polkassembly.io/api/v1/latest-activity/on-chain-posts"
POLKASSEMBLY_POST_DETAILS_URL = "https://api.polkassembly.io/api/v1/posts/on-chain-post"
POLKASSEMBLY_KUSAMA_HEADERS = {
    "x-network": "kusama"
}
POLKASSEMBLY_POLKADOT_HEADERS = {
    "x-network": "polkadot"
}


def prefetch_asana_tasks(project_id: str) -> dict[str, dict]:
    print(f"Caching Asana tasks for project: {project_id}...")

    offset_hash = None
    asana_tasks_map = {}

    while len(asana_tasks_map.keys()) <= ASANA_PREFETCH_TASKS:
        response = requests.get(ASANA_LIST_PROJECT_TASKS_URL % project_id, headers=ASANA_HEADERS, params={
            "opt_fields": "custom_fields",
            "limit": 100,
            **({"offset": offset_hash} if offset_hash else {})
        })

        if response.status_code != 200 or not response.json():
            print(f"Failed to fetch existing tasks from Asana. Check permissions. "
                  f"Status Code: {response.status_code}. Text: {response.text}")
            raise Exception("No access to Asana. Bad API token? Asana is down?")

        data = response.json()

        # map existing tasks to asana_tasks_map
        for task in data.get("data"):
            # map tasks by post_id from "custom_fields"
            for custom_field in task["custom_fields"]:
                if custom_field["gid"] == ASANA_FIELD_POST_ID:
                    asana_tasks_map[custom_field["number_value"]] = task
                    break

        # pagination
        if data.get("next_page"):
            offset_hash = data["next_page"]["offset"]
        else:
            break

    print(f"Total Asana tasks: {len(asana_tasks_map)}")

    return asana_tasks_map


def create_asana_task(data: dict) -> None:
    response = requests.post(
        url=ASANA_CREATE_TASK_URL,
        headers=ASANA_HEADERS,
        json=data
    )

    if response.status_code == 201:
        print(f"Task '{data['data']['name']}' created successfully.")
    else:
        print(f"Failed to create task '{data['data']['name']}'. "
              f"Status Code: {response.status_code}. Text: {response.text}")


def update_asana_task(task_gid, data) -> None:
    response = requests.put(
        url=ASANA_UPDATE_TASK_URL % task_gid,
        headers=ASANA_HEADERS,
        json=data
    )
    if response.status_code == 200:
        print(f"Task '{data['data']['name']}' updated successfully.")
    else:
        print(f"Failed to update task '{data['data']['name']}'. "
              f"Status Code: {response.status_code}. Text: {response.text}")
