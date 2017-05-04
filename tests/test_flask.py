import flask
import time
# import datetime
#
from mock import MagicMock
from concurrent.futures import Future
from werkzeug.datastructures import Headers

from ultron_client.clients import FlaskUltronAsyncService


ULTRON_HEADERS = {
    'Content-Length': 42,
    'AUTHORIZATION': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9',
    'ACCEPT_LANGUAGE': 'en',
    'ACCEPT': 'application/vnd.ajns.kitchenstories+json; version=2.3',
    'CLOUDFRONT_VIEWER_COUNTRY': 'DE',
    'X-Ultron-Test-Group': 'A',
}


def mock_json(*args, **kwargs):
    # time.sleep(0.5)
    return MagicMock(json=MagicMock(return_value={'yeeah': 'json'}))

Future.result = MagicMock(side_effect=mock_json)


class TestFlask(object):
    def setup(self):
        self.app = flask.Flask(__name__)

    @staticmethod
    def _make_ultron_request_header():
        request = flask.request
        request.headers = Headers(ULTRON_HEADERS)
        return request

    def test_request_headers_forwarding(self):
        with self.app.test_request_context('/'):
            request = self._make_ultron_request_header()
            ultron = FlaskUltronAsyncService(request)

            assert ultron.headers['Authorization'] == ULTRON_HEADERS['AUTHORIZATION']
            assert ultron.headers['Accept-Language'] == ULTRON_HEADERS['ACCEPT_LANGUAGE']
            assert ultron.headers['Accept'] == ULTRON_HEADERS['ACCEPT']
            assert ultron.headers['CLOUDFRONT-VIEWER-COUNTRY'] == ULTRON_HEADERS['CLOUDFRONT_VIEWER_COUNTRY']
            assert ultron.headers['X-Ultron-Test-Group'] == ULTRON_HEADERS['X-Ultron-Test-Group']

    def test_fetch_data_is_parallel(self):
        # TODO: If we now how to patch future results - reactivate this
        # with self.app.test_request_context('/'):
        #     start = datetime.datetime.now()
        #
        #     request = self._make_ultron_request_header()
        #     ultron = FlaskUltronAsyncService(request, max_workers=2)
        #     ultron.get('a', 'http://localhost')
        #     ultron.get('b', 'http://localhost')
        #     res = ultron.results()
        #     end = datetime.datetime.now()
        #
        #     print (end-start)
        #     assert (end-start).seconds < 0.5
        pass

    def test_make_flask_response(self):
        with self.app.test_request_context('/'):
            request = self._make_ultron_request_header()
            ultron = FlaskUltronAsyncService(request)
            ultron.get('a', 'http://localhost')
            ultron.results()
            resp = ultron.make_flask_response('hans')

            assert resp.status_code == 200
            assert resp.response == ['hans']

            for h in ultron.resp_headers_copy:
                assert h in resp.headers.keys()

