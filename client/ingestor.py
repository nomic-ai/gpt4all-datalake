import argparse
import csv
import json
from typing import Dict, List

import requests
from rich.progress import track

URL = "https://api.gpt4all.io"


def ingestor(
    conversations: List[Dict],
    source: str = "",
    submitter_id: str = "",
    agent_id: str = "",
):
    headers = {"Content-Type": "application/json"}

    for conversation in conversations:
        json_to_beam = {
            "source": source,
            "submitter_id": submitter_id,
            "agent_id": agent_id,
            "conversation": conversation,
        }

        response = requests.post(
            URL + "/v1/ingest/chat", json=json_to_beam, headers=headers
        )

        if response.status_code > 300:
            print("Request failed with status code:", response.status_code)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Input file to upload to datalake")
    parser.add_argument("input_file", help="The name of the input file")
    args = parser.parse_args()

    with open(args.input_file, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        csv_rows = []

        for row in csv_reader:
            json_object = row

            csv_rows.append(dict(json_object))

    conversations = []
    for idx, item in enumerate(track(csv_rows)):
        json_obj = {"conversation": []}
        try:
            user_obj = {
                "content": eval(item["function_args"])[1]["content"],
                "role": "user",
            }

            assistant_obj = {
                "content": eval(item["request_response"])[0]["content"],
                "role": "assistant",
            }

            json_obj["conversation"].append(user_obj)
            json_obj["conversation"].append(assistant_obj)

            conversations.append(json_obj)
        except:
            print(
                f"Index {idx} of the input data failed to be processed. Skipping to next!"
            )

    ingestor(conversations=conversations, source="promptlayer", submitter_id="YuvaA#23", agent_id= "gpt-3.5-turbo")
