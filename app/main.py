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


async def version(request):
    return JSONResponse({"version": 0})


async def save_click_and_predict_cluster_api(request: NewClickRequest):
    # TODO: fill up
    return NewClickResponse(cluster_idx=0, is_new=True)  # TODO


async def predict_cluster_api(request: NewClickRequest):
    # TODO: fill up
    return PredictClickResponse(cluster_idx=None)  # TODO


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
