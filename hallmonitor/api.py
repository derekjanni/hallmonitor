from flask import Flask
from flask_restful import Resource, Api
from flask import Flask
from resources.health import Health
from resources.endpoint import EndpointResource, GlobalAggregator
import yaml
import hallmonitor.hallmonitor as hallmonitor
import argparse

# API
app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app, catch_all_404s=True)
api.add_resource(HealthResource, '/health')

with open(f'config/config.yaml') as stream:
    config = yaml.safe_load(stream)

test_cases = config.get('test_cases')

if test_cases:
    # Create endpoints that mirror the test_cases in config.yaml
    # Each test case will get its own
    endpoints = [EndpointResource(**test_case) for test_case in test_case]
    for endpoint in endpoints:
        # Config test cases define a mapping between a necessary
        # Name field on test cases and the route the test on the external API
        # As such, you must give test case unique names in order to get a usable
        # Hallmonitor API.
        api.add_resource(endpoint, endpoint.name)

# Add Global Aggregator to get stats on all test_cases

hallmonitor.main(config=config, cli=False, monitor=True)

if __name__ == "__main__":
    app.run(port=5001)
