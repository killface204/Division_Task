import firebase_admin
from firebase_admin import credentials, firestore
import yaml
import requests
import json 

DOC_ID = "doHX26bnzu9iIIKAyVlE"

url = "https://api.doppler.com/v3/configs/config/secret?project=task-automation&config=dev&name=FIREBASE_CREDS"

headers = {
    "accept": "application/json",
    "authorization": "Bearer dp.pt.qrAvsDDw6E8EWeeTUV8LHJ6FKUY19zD7v6a1iV8U5mX "
}

response = requests.get(url, headers=headers)
result = response.json()


# Only initialize once in your process
if not firebase_admin._apps:
    cred = credentials.Certificate(json.loads(result['value']['computed']))
    firebase_admin.initialize_app(cred)

db = firestore.client()

collection = db.collection("Workflow_Configs")

with open("task_config.yaml", "r") as f:
    task_config = yaml.safe_load(f)


def get_input(input_name):
    try:
        response = collection.document(DOC_ID).get([f"inputs.{task_config.get('name')}.{input_name}"]).to_dict()
        input_path = response.get('inputs',{}).get(task_config.get('name'),{}).get(input_name)
        response = collection.document(DOC_ID).get([f"outputs.{input_path}"]).to_dict()
        split = input_path.split('.')
        input_value = response.get('outputs',{}).get(split[0],{}).get(split[1],{})
        return input_value
    except Exception as e:
        print(f"Error retrieving input {input_name}: {e}")
        return None

def set_output(output_name, value):
    try:
        result = collection.document(DOC_ID).update({
            f"outputs.{task_config.get('name')}.{output_name}": value
        })
        return result
    except Exception as e:
        print(f"Error setting output {output_name}: {e}")
        return None