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


## Web API


The dev service is hosted at: htps://taar.dev.mozaws.net

You must include a single GUID as the last segment of a URL encoded
path.

The TAARlite service currently exposes a single URL that can be called
with HTTP GET on the URL path : 

```
    /taarlite/api/v1/addon_recommendations/<your_guid_here>/
```

A sample invocation for the GUID `{some_addon_guid}` using curl would look like this:

```bash
curl https://taar.dev.mozaws.net/taarlite/api/v1/addon_recommendations/%7Bsome_addon_guid%7D/
```

You should get JSON output that appears in this format: 

```json
{"results": ["guid1", "guid2", "guid3", "guid4"]}
```

You may specify an optional normalization mode by passing in a CGI
argument `normalize` using one of the following choices:

* rownorm_sum
* row_count
* row_sum

Generally - you should get the best results using `rownorm_sum`.

Passing in an invalid normalization type will yield an empty `results`
list.

Example :

```bash
curl http://localhost:8000/taarlite/api/v1/addon_recommendations/%7Bsome_addon_guid%7D/?normalize=rownorm_sum
```
