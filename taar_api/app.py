# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from flask import Flask
from flask import request
from dockerflow.flask import Dockerflow

from taar_lite.recommenders import GuidBasedRecommender
from srgutil.context import default_context

import json
from decouple import config
import optparse

app = Flask(__name__)
dockerflow = Dockerflow(app)

VALID_BRANCHES = set(['linear', 'ensemble', 'control'])

TAAR_MAX_RESULTS = config('TAAR_MAX_RESULTS', default=4, cast=int)


class ResourceProxy(object):
    def __init__(self):
        self._resource = None

    def setResource(self, rsrc):
        self._resource = rsrc

    def getResource(self):
        return self._resource


PROXY_MANAGER = ResourceProxy()


@app.route('/taarlite/api/v1/addon_recommendations/<string:guid>/')
def recommendations(guid):
    """Return a list of recommendations provided a telemetry client_id."""
    # Use the module global PROXY_MANAGER
    global PROXY_MANAGER

    if PROXY_MANAGER.getResource() is None:
        ctx = default_context()

        # Lock the context down after we've got basic bits installed
        root_ctx = ctx.child()

        instance = GuidBasedRecommender(root_ctx)
        PROXY_MANAGER.setResource(instance)

    instance = PROXY_MANAGER.getResource()

    normalization_type = request.args.get('normalize', None)

    cdict = {'guid': guid, 'normalize': normalization_type}
    recommendations = instance.recommend(client_data=cdict,
                                         limit=TAAR_MAX_RESULTS)

    if len(recommendations) != TAAR_MAX_RESULTS:
        recommendations = []

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
