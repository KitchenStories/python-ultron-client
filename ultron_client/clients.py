from enum import Enum

from requests_futures.sessions import FuturesSession

from flask import make_response


class FlaskUltronAsyncService(object):
    class Stage(Enum):
        DEV = 'dev'
        BETA = 'beta'
        LIVE = 'live'
        LOCAL = 'local'

    API_STAGES = {
        Stage.LOCAL: 'http://localhost:8000',
        Stage.DEV: 'https://api-dev.kitchenstories.io',
        Stage.BETA: 'https://api-beta.kitchenstories.io',
        Stage.LIVE: 'https://api.kitchenstories.io',
    }

    def __init__(self, request, max_workers=10, stage=Stage.DEV):
        self.headers = {
            'Authorization': request.headers.get('AUTHORIZATION', ''),
            'Accept-Language': request.headers.get('ACCEPT_LANGUAGE', ''),
            'Accept': request.headers.get('ACCEPT', ''),
            'CLOUDFRONT-VIEWER-COUNTRY': request.headers.get('CLOUDFRONT_VIEWER_COUNTRY', ''),
            'X-Ultron-Test-Group': request.headers.get('X-ULTRON-TEST-GROUP', ''),
        }
        self.resp_headers_copy = (
            'Content-Type',
            'X-Ultron-Api-Version',
            'X-Ultron-Version'
        )
        self.server = self.API_STAGES[stage]
        self.session = FuturesSession(max_workers=max_workers)
        self.futures = {}
        self.response_headers = {}

    def get(self, key, url, parameters=None):
        """
        Build future objects for concurrency 

        Args:
            key: this is need for remap response to object, because odering of future 
                    objects is not guaranteed
            url: the url of the resource
            parameters: request get-parameters

        Returns: nothing

        """
        full_url = '{}{}'.format(self.server, url)
        self.futures[key] = self.session.get(full_url, headers=self.headers, params=parameters)

    def results(self):
        """
        Fetches all concurrency objects 

        Returns: Dict {key: request.response.json object}, ulron-headers

        """
        resp_data = {}
        res = {}
        for key, future in self.futures.items():
            res = future.result()
            resp_data[key] = res.json()

        # Copy Ultron headers
        self.response_headers = {x: res.headers[x] for x in self.resp_headers_copy}
        return resp_data

    def make_flask_response(self, content):
        resp = make_response(content)

        # We must overwrite header values
        for k, v in self.response_headers.items():
            resp.headers[k] = v

        return resp
