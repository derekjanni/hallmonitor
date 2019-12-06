from flask_restful import Resource, abort
from flask import request
import services.endpoint as endpoint_service

class EndpointResource(Resource):
    def __init__(self, **kwargs):
        name = f'/{kwargs.get("name")}'
        self._id = sum([ord(x) for x in name])

        self.__name__=name
        self.name=name

    def get(self):
        name = request.path
        idx = sum([ord(x) for x in name])
        return endpoint_service.get_endpoint_stats(idx)

class GlobalAggregator(Resource):
    def get(self):
        return endpoint_service.get_all_endpoint_stats()
