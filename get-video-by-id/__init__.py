import logging

import azure.functions as func
from azure.cosmos import CosmosClient, PartitionKey, partition_key
from azure.storage.blob import BlobServiceClient, BlobClient
import uuid
import json

blobCnnString = 'DefaultEndpointsProtocol=https;AccountName=rossgartland;AccountKey=teSnaZ/VrtRUm+ENzTDsOoTrH+XbXy8DYkm3Iyoq4DV8tNlZqnpGxhvJY0EZD2SQCfoFKK8Jnboa+AStRU8dlA==;EndpointSuffix=core.windows.net'
cosmosEndpoint = 'https://rossgartlandcosmos.documents.azure.com:443/'
cosmosKey = 'dFfKP7CY0mO9DEONIEV3wuWOYYULjpQC75crxAtcgOQQ0kLMyBDV3bA4jk0TmOGAtrz5dHwqXwYAACDb7EAxSQ=='
cosmos = CosmosClient(cosmosEndpoint, cosmosKey)
partition_key = PartitionKey(path='/id')


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    db = cosmos.get_database_client('a2-video-streaming')

    container = db.get_container_client('videos')

    videoID = req.route_params.get("videoID")

    testq = 'SELECT * FROM videos WHERE videos.id = ' + videoID
    video = list(container.query_items(
        query="SELECT * FROM videos WHERE videos.id = @id",
        parameters=[{
            "name": "@id", "value": videoID
        }],
        enable_cross_partition_query=True
    ))

    header = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Methods': 'GET,POST'
    }

    return func.HttpResponse(json.dumps(video), headers=header, mimetype="application/json", status_code=200)
