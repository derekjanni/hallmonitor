from flask_restful import Resource, abort

class HealthResource(Resource):
    def get(self):
        return 'healthy'
