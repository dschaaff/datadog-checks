# Datadog Checks

This is a repo for custom Datadog integrations.

## s3 object count

This check was created to solve a specific problem I had, but may be useful to you as well.

I manage several apps that write various pieces of data to the local file system and rely on fluentd to ship them to s3. There is solid monitoring around the fluentd aggregator process but I wanted better visibility and alerting when things aren’t written to s3 as expected.

The solution I came up with was a custom Datadog check. The files I am monitoring put into a bucket `example-logs/data/<event files>/<year>/<month>/<day>` Each day a new path is setup in the s3 bucket for that day’s date, e.g. `logs/data/example-log/2018/08/15`. My Datadog check sends the count of objects in the days directory as a gauge. You can then monitor that objects are created each day as expected and at a normal rate.

Here is an example config

```yaml
init_config:

instances:
# this will monitor s3://example-logs/data/production/event-log/<year>/<month>/<day>
  - bucket: example-logs
    prefix: data/production/event-log
    tags:
      - 'env:production'
      - 'log:event-log'
  - bucket: example-logs
    prefix: data/staging/event-log
    tags:
      - 'env:staging'
      - 'log:event-log'
```

The check will add the current date path to the prefix automatically. The code for the check is pretty simple.

### Setup

- Install boto3 via the Datadog embedded pip

```bash
/opt/datadog-agent/embedded/bin/pip install boto3
```

- add s3_object_count.py to /etc/datadog-agent/checks.d
- add your config file to /etc/datadog-agent/conf.d/s3_object_count.d
