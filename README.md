# **datumpy**

Welcome to datumpy, a simple RESTful API for storing and retrieving data from various devices.

### Setup

---

To run the application, follow these steps:

1. Clone the repository: `git clone https://github.com/tevfik/datumpy.git`
2. Create a virtual environment: `python -m venv ~/venv/datumpy` (optional but recommended)
3. Activate the virtual environment: `source ~/venv/datumpy/bin/activate` (on Linux/Mac) or `venv\datumpy\Scripts\activate` (on Windows)

### Building and Running with Docker

---

The easiest way to run datumpy is by using Docker. Here's how you can build and run the application:

**Step 1: Build the Docker image**

Run the following command in your terminal:

```
docker build -t datumpy .
```

This will create a new Docker image named `datumpy`.

**Step 2: Run the Docker container**

Run the following command to start a new container from the `datumpy` image:

```bash
docker run -it --rm -p 8000:8000 datum-api
```

This will start a new container and map port 8000 on your local machine to port 8000 in the container.

### Endpoints

---

The Datum API has the following endpoints:

#### Create a new datum for a given device.

* **POST /data/{device_id}** 
  * Request Body: JSON object with a single property `content` (string, max length 140 characters)
  * Response: JSON object with properties `id`, `device_id`, and `content`
  * Test command: `curl -X POST -H "Content-Type: application/json" -d '{"content": "Test content"}' http://localhost:8000/data/123`

* **GET /data/{device_id}?content=str** 
  * Response: JSON object with properties `id`, `device_id`, and `content`
  * Test command: `curl -X GET http://localhost:8000/data/123?content=str`

#### Retrieve all data for a given device.

* **GET /data/{device_id}** 
  * Response: Array of JSON objects with properties `id`, `device_id`, and `content`
  * Test command: `curl -X GET http://localhost:8000/data/123`

#### Retrieve the last N data points for a given device.

* **GET /data/{device_id}/last/{n}** 
  * Response: Array of JSON objects with properties `id`, `device_id`, and `content`
  * Test command: `curl -X GET http://localhost:8000/data/123/last/5`

#### Retrieve all data for a given device since a specified timestamp (inclusive).

* **GET /data/{device_id}/since/{t1}** 
  * Request Parameter: `t1` - timestamp in ISO 8601 format (eg. 2022-01-01T12:00:00Z)
  * Response: Array of JSON objects with properties `id`, `device_id`, and `content`
  * Test command: `curl -X GET http://localhost:8000/data/123/since/2022-01-01T12%3A00%3A00Z`

#### Retrieve all data for a given device between two specified timestamps (inclusive).

* **GET /data/{device_id}/between/{t1}/{t2}** 
  * Request Parameters: 
    * `t1` - start timestamp in ISO 8601 format (eg. 2022-01-01T12:00:00Z)
    * `t2` - end timestamp in ISO 8601 format (eg. 2022-01-02T12:00:00Z)
  * Response: Array of JSON objects with properties `id`, `device_id`, and `content`
  * Test command: `curl -X GET http://localhost:8000/data/123/between/2022-01-01T12%3A00%3A00Z/2022-01-02T12%3A00%3A00Z`

#### Retrieve a specific datum by ID.

* **GET /data/{device_id}/{datum_id}** 
  * Response: JSON object with properties `id`, `device_id`, and `content`
  * Test command: `curl -X GET http://localhost:8000/data/123/456`
