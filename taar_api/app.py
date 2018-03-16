# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from flask import Flask
from flask import request
from dockerflow.flask import Dockerflow

from taar import recommenders
from taar.context import default_context
from taar.profile_fetcher import ProfileFetcher
from taar import ProfileController
import json
from decouple import config
import optparse

app = Flask(__name__)
dockerflow = Dockerflow(app)

VALID_BRANCHES = set(['linear', 'ensemble', 'control'])

DYNAMO_REGION = config('DYNAMO_REGION', default='us-west-2')
DYNAMO_TABLE_NAME = config('DYNAMO_TABLE_NAME', default='taar_addon_data_20180206')
TAAR_MAX_RESULTS = config('TAAR_MAX_RESULTS', default=10, cast=int)


class ResourceProxy(object):
    def __init__(self):
        self._resource = None

    def setResource(self, rsrc):
        self._resource = rsrc

    def getResource(self):
        return self._resource


PROXY_MANAGER = ResourceProxy()


@app.route('/api/recommendations/<uuid:uuid_client_id>/')
def recommendations(uuid_client_id):
    """Return a list of recommendations provided a telemetry client_id."""
    # Use the module global PROXY_MANAGER
    global PROXY_MANAGER

    # Coerce the uuid.UUID type into a string
    client_id = str(uuid_client_id)

    branch = request.args.get('branch', '')

    if branch.endswith('-taar'):
        branch = branch.replace("-taar", "")

    if branch not in VALID_BRANCHES:
        # Force branch to be a control branch if an invalid request
        # comes in.
        branch = 'control'

    extra_data = {'branch': branch}

    locale = request.args.get('locale', None)
    if locale is not None:
        extra_data['locale'] = locale

    platform = request.args.get('platform', None)
    if platform is not None:
        extra_data['platform'] = platform

    if PROXY_MANAGER.getResource() is None:
        ctx = default_context()
        dynamo_client = ProfileController(region_name=DYNAMO_REGION,
                                          table_name=DYNAMO_TABLE_NAME)
        profile_fetcher = ProfileFetcher(dynamo_client)

        ctx['profile_fetcher'] = profile_fetcher

        # Lock the context down after we've got basic bits installed
        root_ctx = ctx.child()
        r_factory = recommenders.RecommenderFactory(root_ctx)
        root_ctx['recommender_factory'] = r_factory
        instance = recommenders.RecommendationManager(root_ctx.child())
        PROXY_MANAGER.setResource(instance)

    instance = PROXY_MANAGER.getResource()
    recommendations = instance.recommend(client_id=client_id,
                                         limit=TAAR_MAX_RESULTS,
                                         extra_data=extra_data)
    # Strip out weights from TAAR results to maintain compatibility
    # with TAAR 1.0
    jdata = {"results": [x[0] for x in recommendations]}

    response = app.response_class(
            response=json.dumps(jdata),
            status=200,
            mimetype='application/json'
            )
    return response


def flaskrun(app, default_host="127.0.0.1", default_port="8000"):
    """
    Takes a flask.Flask instance and runs it. Parses
    command-line flags to configure the app.
    """

    # Set up the command-line options
    parser = optparse.OptionParser()
    parser.add_option("-H", "--host",
                      help="Hostname of the Flask app " +
                           "[default %s]" % default_host,
                      default=default_host)
    parser.add_option("-P", "--port",
                      help="Port for the Flask app " +
                           "[default %s]" % default_port,
                      default=default_port)

    # Two options useful for debugging purposes, but
    # a bit dangerous so not exposed in the help message.
    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug",
                      help=optparse.SUPPRESS_HELP)
    parser.add_option("-p", "--profile",
                      action="store_true", dest="profile",
                      help=optparse.SUPPRESS_HELP)

    options, _ = parser.parse_args()

    # If the user selects the profiling option, then we need
    # to do a little extra setup
    if options.profile:
        from werkzeug.contrib.profiler import ProfilerMiddleware

        app.config['PROFILE'] = True
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
        options.debug = True

    app.run(
        debug=options.debug,
        host=options.host,
        port=int(options.port)
    )


if __name__ == '__main__':
    flaskrun(app)
