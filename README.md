# TAAR API-lite

[![CircleCI](https://circleci.com/gh/mozilla/taar-api-lite.svg?style=shield)](https://circleci.com/gh/mozilla/taar-api-lite)
[![codecov](https://codecov.io/gh/mozilla/taar-api-lite/branch/master/graph/badge.svg)](https://codecov.io/gh/mozilla/taar-api-lite)


## Instructions for development

0. Make sure you have [docker](https://docker.io) and [docker-compose](https://github.com/docker/compose)
1. make up

## Instructions for deployment

The target environment for this project follows the [dockerflow](https://github.com/mozilla-services/Dockerflow) conventions.
In order to run it correctly, a number of environment variables needs to be set up.
The full list of variables can be found in the web section of the docker-compose.yml file.
From a services standpoint, this project requires:
 - an optional Redis cache service, defined by CACHE_URL

### Updating Taar

The core of taar-service lives in the [mozilla-taarlite](https://pypi.python.org/pypi/mozilla-taarlite) python package.
These are the steps required to deploy a new version of mozilla-taarlite on taar-api-lite using [hashin](https://pypi.python.org/pypi/hashin):

From the root of the repository:

```bash
hashin mozilla-taarlite==<major>.<minor>.<patch>
```
Then open a pull request with the changes to requirements.txt. Once
it's merged to master, the service will automatically update.
