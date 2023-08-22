This code uses **`DBSCAN`** from the sklearn.cluster module to perform clustering on click data. 

---

`Class ClusterClicks`: 
The ClusterClicks class performs DBSCAN clustering on the provided click data. It has the following attributes

`clustering`: An instance of **`DBSCAN`** from the sklearn.cluster module used for clustering.
`clusters`: The result of the clustering fit.
`cluster_id`: The cluster label of the last sample.
And the following method:

`fit`: Perform DBSCAN clustering on the provided click data and return the cluster label of the last sample.

Function `save_click_and_predict_cluster_api`:
This function accepts a request object of type `NewClickRequest` and a database session object. The function processes the incoming request and adds the new click data to the database and stores the click's coordinates in memory in the form of a list. Then the function performs clustering on the stored click data for the specific page ID and returns a response object of type `NewClickResponse` containing the cluster index and a flag indicating whether the cluster is new or not.

Function `predict_cluster_api`:
This function accepts a request object of type `NewClickRequest`. The function processes the incoming request and extracts coordinates and `page_id` from it, stores the click's coordinates in memory in the form of a list. The function then clusters the incoming coordinates per `page_id` and returns a `cluster_id` that the input coordinates belong to.

--- 

**_NOTE:_** In this code, the global variable `clicks` stores the click data and `clusters` stores the result of the clustering fit, ordered by `page_id`.

---

## What's included
- FastAPI (examples in `app/main.py`)
- SQLAlchemy (models in `app/db_models.py`)
- PostgreSQL
- NumPy


## Getting started

0) Install Docker
1) Clone the repository
2) Use `docker-compose up` in your Terminal to start the Docker container.
3) The app is defaulted to run on `localhost:8004`
   * `/`: The root url (contents from `app/main.py`)

## Rebuild infrastructure (not for code changes)
- `docker-compose build`

## Troubleshooting
- `docker-compose down` (This will destroy all your containers for the project, might need it when you change db models)
- `docker-compose up`

### __Infrastructure changes__
I had to make these changes to ensure that the app could be setup:

* To resolve the following error during initial setup: 
```
ERROR [internal] load metadata for docker.io/tiangolo/uvicorn-gunicorn-fastapi:python3.8
```

- Change Docker image from `tiangolo/uvicorn-gunicorn-fastapi:python3.8 `to `tiangolo/uvicorn-gunicorn-fastapi:python3.10`. 

- `@contextmanager` decorator was changed to a function in `instance.py` as without it, the `CREATE TABLE` was failing. 
- Also changed database `id` to not include `uuid_generate_v4()` function as PostgreSQL gave a function not found error. Subsequent change to `gen_random_uuid()` also failed so resorted to using `autoincrement` for `PRIMARY KEY`
- Changed the APIRoute from `/save_click_and_predict_cluster` to `/new_click` per the files in `tests/cases/test_cases_XX.json`


## Running tests
### Installation
```bash
python3 -m pip install requests
```

### Run test cases
```bash
python3 tests/test.py
```

---

**_NOTE:_** Due to the use of DBSCAN and it's parameters specifically `eps`, which determines how close points should be to each other to be considered a part of a cluster and `min_samples`, which indicates the number of neighbouring points required for a point to be considered as a dense region, or a valid cluster; the clusters created though valid do not conform to the test_cases. Further discussion on these settings are required. 
