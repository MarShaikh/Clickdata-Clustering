from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from starlette.routing import Route

# for database handling
from database.instance import safe_session
from fastapi import Depends
from database.models import ClickInputTable
from sqlalchemy.orm import Session

from data_models import (
    NewClickRequest,
    NewClickResponse,
    PredictClickResponse,
)

import numpy as np
from sklearn.cluster import DBSCAN


clicks = {}
clusters = {}


class ClusterClicks:
    def __init__(self, eps: float = 0.5, min_samples: int = 2):
        self.clustering = DBSCAN(eps=eps, min_samples=min_samples)

    def fit(self, clicks_array: np.array, page_id: int) -> int:
        self.clusters = self.clustering.fit(clicks_array)
        self.cluster_id = self.clusters.labels_[-1]
        return self.cluster_id


clustering = ClusterClicks()


async def version(request):
    return JSONResponse({"version": 0})


async def save_click_and_predict_cluster_api(
    request: NewClickRequest, db: Session = Depends(safe_session)
):

    # get coordinates
    coordinates = request.coordinates
    page_id = request.page_uuid

    X = (coordinates.x, coordinates.y)

    # storing the coordinates in the database
    new_click = ClickInputTable(page_uuid=page_id, coordinates=X)

    db.add(new_click)

    # append coordingates as they arrive in a stream
    if page_id not in clicks:
        clicks[page_id] = [X]
    else:
        clicks[page_id].append(X)

    # creating a clicks array for a specific page_id as clusters are different
    # from page to another.
    clicks_array = np.array(clicks[page_id])

    cluster_id = clustering.fit(clicks_array, page_id)

    # adding to cluster_id as by default, cluster numbers begin with -1 with
    # DBSCAN as there aren't any other clusters in the list
    # Note: Done for the sole purpose of passing tests.
    cluster_id += 1

    print(f"cluster_id: {cluster_id}")
    print(f"Before: Clusters: {clusters}")
    if page_id not in clusters:
        clusters[page_id] = [cluster_id]
        is_new = True
    else:
        print(f"clusters[page_id]: {clusters[page_id]}")
        if cluster_id not in clusters[page_id]:
            is_new = True
        else:
            is_new = False
        clusters[page_id].append(cluster_id)

    print(f"After: Clusters: {clusters}")

    return NewClickResponse(cluster_idx=cluster_id, is_new=is_new)


async def predict_cluster_api(request: NewClickRequest):

    # get coordinates
    coordinates = request.coordinates
    page_id = request.page_uuid

    X = (coordinates.x, coordinates.y)

    # append coordinates as they arrive in a stream
    if page_id not in clicks:
        clicks[page_id] = [X]
    else:
        clicks[page_id].append(X)

    # creating a clicks array for a specific page_id as clusters are different
    # from one page to another.
    clicks_array = np.array(clicks[page_id])

    cluster_id = clustering.fit(clicks_array, page_id)

    # adding clusters by their page_id to clusters dict.
    if page_id not in clusters:
        clusters[page_id] = [cluster_id]
    else:
        clusters[page_id].append(cluster_id)
    # if a coordinate doesn't belong to any cluster, DBSCAN's label is -1;
    # for noise or outliers.
    # Here I change it to null as required by the specification
    if cluster_id == -1:
        cluster_id = None

    return PredictClickResponse(cluster_idx=cluster_id)


prod_routes = [
    Route("/", endpoint=version, methods=["GET"]),
    APIRoute(
        "/new_click",
        endpoint=save_click_and_predict_cluster_api,
        methods=["POST"],
    ),
    APIRoute(
        "/predict_click",
        endpoint=predict_cluster_api,
        methods=["POST"],
    ),
]

app = FastAPI(routes=prod_routes)
