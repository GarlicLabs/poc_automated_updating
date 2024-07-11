import requests
import json
from time import sleep
from datetime import datetime
import sys

API_TOKEN = sys.argv[1]

DROPLETS_URL = "https://api.digitalocean.com/v2/droplets"
SNAPSHOTS_URL = "https://api.digitalocean.com/v2/snapshots"

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def list_droplets():
    response = requests.get(DROPLETS_URL, headers=HEADERS)
    return response.json()

def create_snapshot(droplet_id):
    snapshot_name = f"snapshot-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    data = {
        "type": "snapshot",
        "name": snapshot_name
    }
    response = requests.post(f"{DROPLETS_URL}/{droplet_id}/actions", headers=HEADERS, data=json.dumps(data))
    return response.json()

def list_snapshots():
    response = requests.get(f"{SNAPSHOTS_URL}?resource_type=droplet", headers=HEADERS)
    return response.json()

def delete_snapshot(snapshot_id):
    response = requests.delete(f"{SNAPSHOTS_URL}/{snapshot_id}", headers=HEADERS)
    return response.status_code == 204

def main():

    droplets = list_droplets().get('droplets', [])

    for droplet in droplets:
        droplet_id = droplet['id']
        droplet_name = droplet['name']

        print(f"Creating snapshot for droplet: {droplet_name} (ID: {droplet_id})")
        create_snapshot(droplet_id)

        sleep(10)

        snapshots = list_snapshots().get('snapshots', [])
        droplet_snapshots = [snap for snap in snapshots if snap['resource_id'] == droplet_id]

        if len(droplet_snapshots) > 1:
            oldest_snapshot = min(droplet_snapshots, key=lambda x: x['created_at'])
            oldest_snapshot_id = oldest_snapshot['id']
            print(f"Deleting oldest snapshot: {oldest_snapshot_id} for droplet: {droplet_name} (ID: {droplet_id})")
            delete_snapshot(oldest_snapshot_id)

if __name__ == "__main__":
    main()