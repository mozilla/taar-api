# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from flask import Flask
from dockerflow.flask import Dockerflow
import optparse
from decouple import config
import importlib

app = Flask(__name__)
dockerflow = Dockerflow(app)


def flaskrun(app, default_host="127.0.0.1", default_port="8000"):
    """
    Takes a flask.Flask instance and runs it. Parses
    command-line flags to configure the app.
    """

    # Set up the command-line options
    parser = optparse.OptionParser()
    parser.add_option(
        "-H",
        "--host",
        help="Hostname of the Flask app " + "[default %s]" % default_host,
        default=default_host,
    )
    parser.add_option(
        "-P",
        "--port",
        help="Port for the Flask app " + "[default %s]" % default_port,
        default=default_port,
    )

    # Two options useful for debugging purposes, but
    # a bit dangerous so not exposed in the help message.
    parser.add_option(
        "-d", "--debug", action="store_true", dest="debug", help=optparse.SUPPRESS_HELP
    )
    parser.add_option(
        "-p",
        "--profile",
        action="store_true",
        dest="profile",
        help=optparse.SUPPRESS_HELP,
    )

    options, _ = parser.parse_args()

    # If the user selects the profiling option, then we need
    # to do a little extra setup
    if options.profile:
        from werkzeug.contrib.profiler import ProfilerMiddleware

        app.config["PROFILE"] = True
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
        options.debug = True

    app.run(debug=options.debug, host=options.host, port=int(options.port))


# TODO: move everything below here into the plugin

APP_PLUGIN = config("TAAR_API_PLUGIN", default="")
if APP_PLUGIN != "":
    plugin = importlib.import_module(APP_PLUGIN)
    configure_plugin = plugin.configure_plugin
    configure_plugin(app)
else:
    import sys

    sys.stderr.write("Warning - no application is defined.\n")


if __name__ == "__main__":
    flaskrun(app)
