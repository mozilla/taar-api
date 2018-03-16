# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from flask import Flask
from dockerflow.flask import Dockerflow
import json

app = Flask(__name__)
dockerflow = Dockerflow(app)


@app.route('/api/recommendations/<uuid:client_id>/')
def recommendations(client_id):
    response = app.response_class(
            response=json.dumps({'result': "Flask Dockerized"}),
            status=200,
            mimetype='application/json'
            )
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
