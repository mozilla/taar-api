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

app = Flask(__name__)
dockerflow = Dockerflow(app)

VALID_BRANCHES = set(['linear', 'ensemble', 'control'])


class ResourceProxy(object):
    def __init__(self):
        self._resource = None

    def setResource(self, rsrc):
        self._resource = rsrc

    def getResource(self):
        return self._resource


PROXY_MANAGER = ResourceProxy()


@app.route('/api/recommendations/<uuid:client_id>/')
def recommendations(client_id):
    """Return a list of recommendations provided a telemetry client_id."""
    # Use the module global PROXY_MANAGER
    global PROXY_MANAGER

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
        # TODO: fix this with config
        dynamo_client = ProfileController(region_name='us-west-2',
                                          table_name='taar_addon_data_20180206')
        profile_fetcher = ProfileFetcher(dynamo_client)

        ctx['profile_fetcher'] = profile_fetcher

        # Lock the context down after we've got basic bits installed
        root_ctx = ctx.child()
        r_factory = recommenders.RecommenderFactory(root_ctx)
        root_ctx['recommender_factory'] = r_factory
        instance = recommenders.RecommendationManager(root_ctx.child())
        PROXY_MANAGER.setResource(instance)

    instance = PROXY_MANAGER.getResource()
    # TODO: fix the 10 with config
    recommendations = instance.recommend(client_id=client_id,
                                         limit=10,
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
