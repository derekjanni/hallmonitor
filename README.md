# hallmonitor

`hallmonitor` is a configuration-based tool for integration testing your APIs! No more manual clicking or pasting Auth tokens into Postman! Instead, just fill out your configuration files and go.

## How to
- Install with `python setup.py install`
- Fire up `examples/helloworld/api.py`
- `hallmonitor -f examples/helloworld/config.yaml`
- Observe!
- Try it with your own API?

## Future releases
- Deployable hallmonitor that consumes config and constantly tests endpoints for breakage
- Slack integration
- Dashboard for code quality metrics
