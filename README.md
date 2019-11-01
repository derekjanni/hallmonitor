# Hallmonitor

`hallmonitor` is a configuration-based tool for integration testing your APIs! No more manual clicking or pasting Auth tokens into Postman! Instead, just fill out your configuration files and go.

## How to..
- Install with `python setup.py install`
- Fire up `examples/helloworld/api.py`
- `hallmonitor -f examples/helloworld/config.yaml`
- Observe!
- Try it with your own API?

## More in depth

This needs better documentation and enforcement but the current supported `.yaml` fields are shown below. The only supported auth service is currently `auth0` but this can be appended or custom-coded to support many use-cases.

```
addons:
  - name: auth0
    action: auth_header
    url:
    audience:
    grant_type:
    client_id: ${CLIENT_TOKEN}
    client_secret: ${CLIENT_SECRET}
test_cases:
  - description: Do things!
    base: http://dev-server-url:5000/things
    route: /thing
    json: false
    outfile: example.csv
    params:
        param1: 1
        param2: 23
        param3: hello!
```


## Future releases
- Deployable hallmonitor that consumes config and constantly tests endpoints for breakage
- Slack integration
- Dashboard for code quality metrics
