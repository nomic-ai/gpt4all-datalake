import argparse
import json
import csv
from typing import List
from rich.progress import track
import requests

url = "https://api.gpt4all.io/"

def ingestor(documents: List[dict]):
    headers = {'Content-Type': 'application/json'}

    for idx, item in enumerate(documents):
        if idx < 1:
            response = requests.post(url, json=item, headers=headers)

            if response.status_code >= 200 and response.status_code < 300:
                print("Request successful!")
            else:
                print("Request failed with status code:", response.status_code)
                print(json.dumps(item, indent=2))
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Input file to upload to datalake')
    parser.add_argument('input_file', help='The name of the input file')
    args = parser.parse_args()

    with open(args.input_file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        csv_rows = []

        for row in csv_reader:
            json_object = row

            csv_rows.append(dict(json_object))
        
    documents = []
    for idx, item in enumerate(track(csv_rows)):
        json_obj = {}
        try:
            user_obj = {
                "content": eval(item["function_args"])[1]["content"],
                "role": "user",
            }

            assistant_obj = {
                "content": eval(item["request_response"])[0]["content"],
                "role": "assistant",
            }

            json_obj["source"] = "prompt-layer"
            json_obj["submitter_id"] = "YuvaneshA#23"
            json_obj["agent_id"] = item["engine"]
            json_obj["conversation"] = []
            json_obj["conversation"].append(user_obj)
            json_obj["conversation"].append(assistant_obj)

            documents.append(json_obj)
        except:
            continue

    ingestor(documents=documents)
