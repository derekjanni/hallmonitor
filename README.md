# hallmonitor

`hallmonitor` is a configuration-based tool for integration testing your APIs! No more manual clicking or pasting Auth tokens into Postman! Instead, just fill out your configuration files and go.

## how to
- Install necessary dependencies
- Fire up `examples/helloworld/api.py`
- `python hallmonitor/hallmonitor.py -f examples/helloworld/config.yaml`
- Observe!

## future releases
- Deployable hallmonitor that consumes config and constantly tests endpoints for breakage
- Slack integration
- Dashboard for code quality metrics
