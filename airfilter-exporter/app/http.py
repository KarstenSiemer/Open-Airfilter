"""
import traceback
HTTP API for airfilter prometheus collector.
"""

import time
from prometheus_client import CONTENT_TYPE_LATEST, Summary, Counter, generate_latest
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import InternalServerError
from app.collector import collect_sensors

class AirfilterExporterApplication(object):
    """
    Airfilter prometheus collector HTTP handler.
    """

    def __init__(self, duration, errors):
        self._duration = duration
        self._errors = errors

        self._url_map = Map([
            Rule('/', endpoint='index'),
            Rule('/metrics', endpoint='metrics'),
            Rule('/sensors', endpoint='sensors'),
        ])

        self._args = {
            'sensors': ['sds011', 'sleep', 'ccs811']
        }

        self._views = {
            'index': self.on_index,
            'metrics': self.on_metrics,
            'sensors': self.on_sensors,
        }

    def on_sensors(self, sds011='/dev/ttyUSB0', sleep=15, ccs811='false'):
        """
        Request handler for /sensors route
        """

        start = time.time()
        output = collect_sensors(sds011, sleep, ccs811)
        response = Response(output)
        response.headers['content-type'] = CONTENT_TYPE_LATEST
        self._duration.observe(time.time() - start)

        return response

    def on_metrics(self):
        """
        Request handler for /metrics route
        """

        response = Response(generate_latest())
        response.headers['content-type'] = CONTENT_TYPE_LATEST

        return response

    def on_index(self):
        """
        Request handler for index route (/).
        """

        response = Response(
            """<html>
            <head><title>Airfilter Exporter</title></head>
            <body>
            <h1>Airfilter Exporter</h1>
            <p>Visit <code>/sensors?sds011="/dev/ttyUSB0"&sleep="15"</code> to use.</p>
            </body>
            </html>"""
        )
        response.headers['content-type'] = 'text/html'

        return response

    def view(self, endpoint, values, args):
        """
        Werkzeug views mapping method.
        """

        params = dict(values)
        if endpoint in self._args:
            params.update({key: args[key] for key in self._args[endpoint] if key in args})

        try:
            return self._views[endpoint](**params)
        except Exception as error:
            self._errors.inc()
            raise InternalServerError(error)

    @Request.application
    def __call__(self, request):
        urls = self._url_map.bind_to_environ(request.environ)
        view_func = lambda endpoint, values: self.view(endpoint, values, request.args)
        return urls.dispatch(view_func, catch_http_exceptions=True)


def start_http_server(port, address=''):
    """
    Start a HTTP API server for airfilter prometheus collector.
    """

    duration = Summary(
        'airfilter_collection_duration_seconds',
        'Duration of collections by the airfilter exporter',
    )
    errors = Counter(
        'airfilter_request_errors_total',
        'Errors in requests to airfilter exporter',
    )

    # Initialize metrics.
    errors
    duration

    app = AirfilterExporterApplication(duration, errors)
    run_simple(address, port, app, threaded=True, use_debugger=True)
