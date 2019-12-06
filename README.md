# Hallmonitor

`hallmonitor` is a configuration-based tool for integration testing your APIs! No more manual clicking or pasting Auth tokens into Postman! Instead, just fill out your configuration files and go.

## How to..
- Install with `pip install hallmonitor`
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
    name: thing_test
    base: http://dev-server-url:5000/things
    expect:
      status_code: 200
      message: It works!
      json: "{'stringified_json': 'object'}"
      on_fail: "continue" | "quit" # these are your only options
    route: /thing
    json: false
    method: GET
    outfile: example.csv
    params:
        param1: 1
        param2: 23
        param3: hello!
```

# Data storage and collection

If you're deploying this on docker, it will run a local sqlite install to collect stats while
running in API mode. In the future, this may be updated to support longer-term stats storage, but the current
goal is to build a simple frontend on this and just be able to show stats about a given service. 


## Future releases
- Deployable hallmonitor that consumes config and constantly tests endpoints for breakage
- Slack integration
- Dashboard for code quality metrics

[hallmonitor](https://i.pinimg.com/originals/99/dd/44/99dd445c0549fbcf7783737ff1edee10.jpg)
