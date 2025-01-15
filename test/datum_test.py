import requests

# Base URL of the API
BASE_URL = 'http://localhost:8000'

def create_datum(device_id, content):
    url = f"{BASE_URL}/data/{device_id}"
    response = requests.post(url, json={"content": content})
    assert response.status_code == 200
    data = response.json()
    print(f"Created datum with ID {data['id']} for device {device_id}")
    return data

def retrieve_all_data(device_id):
    url = f"{BASE_URL}/data/{device_id}"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    print(f"Retrieved all data for device {device_id}: {data}")

def last_n_data_points(device_id, n):
    url = f"{BASE_URL}/data/{device_id}/last/{n}"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    print(f"Retrieved the last {n} data points for device {device_id}: {data}")

def retrieve_data_since(device_id, timestamp):
    url = f"{BASE_URL}/data/{device_id}/since/{timestamp}"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    print(f"Retrieved all data for device {device_id} since {timestamp}: {data}")

def retrieve_data_between(device_id, start_timestamp, end_timestamp):
    url = f"{BASE_URL}/data/{device_id}/between/{start_timestamp}/{end_timestamp}"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    print(f"Retrieved all data for device {device_id} between {start_timestamp} and {end_timestamp}: {data}")

def retrieve_specific_datum(device_id, datum_id):
    url = f"{BASE_URL}/data/{device_id}/{datum_id}"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    print(f"Retrieved specific datum with ID {datum_id} for device {device_id}: {data}")

# Example test execution
if __name__ == "__main__":
    # Set up example device and timestamps (modify as needed to reflect real testing conditions)
    DEVICE_ID = '123'
    TIMESTAMP_1 = '2024-01-01T12:00:00Z'
    TIMESTAMP_2 = '2025-01-20T12:00:00Z'

    # Create data
    datum_data = create_datum(DEVICE_ID, "Test content 1")
    datum_data = create_datum(DEVICE_ID, "Test content 2")
    datum_data = create_datum(DEVICE_ID, "Test content 3")
    datum_data = create_datum(DEVICE_ID, "Test content 4")
    datum_data = create_datum(DEVICE_ID, "Test content 5")
    
    # Retrieve all data for device
    retrieve_all_data(DEVICE_ID)
    
    # Retrieve the last N data points (e.g., 5) for a given device
    last_n_data_points(DEVICE_ID, 5)

    # Retrieve data since a specified timestamp
    retrieve_data_since(DEVICE_ID, TIMESTAMP_1)

    # Retrieve data between two timestamps
    retrieve_data_between(DEVICE_ID, TIMESTAMP_1, TIMESTAMP_2)
    
    # Retrieve specific datum by ID (assuming 'datum_id' from the created data or existing records in your system)
    if datum_data:
        retrieve_specific_datum(DEVICE_ID, datum_data['id'])