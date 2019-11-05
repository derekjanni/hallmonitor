import services.endpoint as endpoint_service

class EndpointResource(Resource):
    def __init__(self, **kwargs):
        self._id=hash(str(kwargs))
        self.route=route
        name = kwargs.get('name')

        if name:
            self.__name__=name
            self.name=name
        else:
            self.__name__=id
            self.name=id

    def get(self):
        return endpoint_service.get_endpoint_stats(self._id)

class GlobalAggregator(Resource):
    def get(self):
        return endpoint_service.get_all_endpoint_stats()
