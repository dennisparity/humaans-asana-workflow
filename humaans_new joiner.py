import requests

from common import ASANA_FIELD_URL, ASANA_FIELD_POST_ID, \
    ASANA_FIELD_Probabtion Period, ASANA_FIELD_Entity, ASANA_FIELD_Type, ASANA_FIELD_STATUS, ASANA_FIELD_TOPIC, \
    ASANA_FIELD_PROPOSED_AT, POLKASSEMBLY_ALL_POST_LIST_URL, POLKASSEMBLY_POST_DETAILS_URL, POLKASSEMBLY_POLKADOT_HEADERS, \
    prefetch_asana_tasks, create_asana_task, update_asana_task, ASANA_FIELD_TRACK_NAME_MAPPING, \
    ASANA_FIELD_STATUS_MAPPING

# Asana API
ASANA_PROJECT_ID = "1208107121023942"

# Humaans API
Humaans_= "TBC"
Humaans_LISTING_LIMIT = 100


def fetch_proposals() -> list:
    print(f"Parsing latest new joiner...")

    response = requests.get(POLKASSEMBLY_ALL_POST_LIST_URL, params={
        "listingLimit": POLKASSEMBLY_LISTING_LIMIT,
        "govType": "open_gov",
        "sortBy": "newest"
    }, headers=POLKASSEMBLY_POLKADOT_HEADERS)

    if response.status_code != 200:
        print(
            f"Failed to fetch proposals. Status Code: {response.status_code}. Response: {response.text}")
        return []

    print(f"Loaded {len(response.json()['posts'])} latest proposals")

    proposals = []
    for post in response.json()["posts"]:
        if post["type"] != "ReferendumV2":
            continue

        print(f"Parsing details for post {post['post_id']}...")
        post_details = requests.get(POLKASSEMBLY_POST_DETAILS_URL, params={
            "postId": post["post_id"],
            "proposalType": POLKASSEMBLY_PROPOSAL_TYPE
        }, headers=POLKASSEMBLY_POLKADOT_HEADERS).json()
        post["post"] = post_details

        proposals.append(post)

    return proposals


def format_asana_task_data(referendum, project_id=None) -> dict:
    data = {
        "data": {
            "name": f"{referendum['post_id']}: {referendum['post']['title'] or 'NO TITLE'}",
            "notes": f"{referendum['post']['content'] or ''}",
            "custom_fields": {
                ASANA_FIELD_URL: f"https://polkadot.polkassembly.io/referenda/{referendum['post_id']}",
                ASANA_FIELD_DOT: planck_to_dot(referendum["post"].get("requested")) or 0,
                ASANA_FIELD_POST_ID: referendum["post_id"],
                ASANA_FIELD_PROPOSER: referendum["proposer"],
                ASANA_FIELD_TRACK_NAME: ASANA_FIELD_TRACK_NAME_MAPPING.get(referendum["track_number"]),
                ASANA_FIELD_STATUS: ASANA_FIELD_STATUS_MAPPING.get(referendum["status"]),
                ASANA_FIELD_TOPIC: referendum["post"].get("topic", {}).get("name"),
                ASANA_FIELD_PROPOSED_AT: {
                    "date_time": datetime_to_ISO_8601(referendum["created_at"])
                },
            },
        }
    }

    if project_id:
        data["data"]["projects"] = [project_id]

    return data


def main():
    # cache existing asana tasks for faster "referendum <-> task" mapping
    asana_tasks_cache = prefetch_asana_tasks(project_id=ASANA_PROJECT_ID)

    # fetch referendums from specified tracks
    referendums = fetch_proposals()
    if not referendums:
        print(f"No new referendums found")

    # create or update asana tasks based on referendum post_id
    for referendum in referendums:
        existing_asana_task = asana_tasks_cache.get(referendum["post_id"])
        if existing_asana_task:
            update_asana_task(
                task_gid=existing_asana_task["gid"],
                data=format_asana_task_data(referendum)
            )
        else:
            create_asana_task(
                data=format_asana_task_data(
                    referendum, project_id=ASANA_PROJECT_ID)
            )


if __name__ == "__main__":
    main()
