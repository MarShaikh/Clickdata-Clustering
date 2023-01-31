from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from starlette.routing import Route

from data_models import (
    NewClickRequest,
    NewClickResponse,
    GetBestClusterResponse,
    PredictClickResponse,
    GetBestClusterRequest,
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

        if page_id not in clusters:
            clusters[page_id] = [self.cluster_id]
        else:
            clusters[page_id].append(self.cluster_id)
        
        return self.cluster_id


clustering = ClusterClicks()


async def version(request):
    return JSONResponse({"version": 0})


async def save_click_and_predict_cluster_api(request: NewClickRequest):
    # TODO: fill up
    return NewClickResponse(cluster_idx=0, is_new=True)  # TODO


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

    # creating a clicks array for a specific page_id as clusters are different from one page to another.
    clicks_array = np.array(clicks[page_id])


    cluster_id = clustering.fit(clicks_array, page_id)
        
    return PredictClickResponse(cluster_idx=cluster_id)


# async def get_best_cluster_api(request: GetBestClusterRequest):
#     # TODO: optional
#     return GetBestClusterResponse()


prod_routes = [
    Route("/", endpoint=version, methods=["GET"]),
    APIRoute(
        "/save_click_and_predict_cluster",
        endpoint=save_click_and_predict_cluster_api,
        methods=["POST"],
    ),
    APIRoute(
        "/predict_click",
        endpoint=predict_cluster_api,
        methods=["POST"],
    ),
    # APIRoute("/get_best_cluster", endpoint=get_best_cluster_api, methods=["GET"]),
]

app = FastAPI(routes=prod_routes)
