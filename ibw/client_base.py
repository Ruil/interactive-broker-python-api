import logging
import urllib
from typing import Dict

import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

import ibw.client_utils as client_utils

urllib3.disable_warnings(category=InsecureRequestWarning)

logging.basicConfig(
    filename='app.log',
    format='%(levelname)s - %(name)s - %(message)s',
    level=logging.DEBUG
)


class IBBase:

    def __init__(self) -> None:
        self.api_version = 'v1/'

        # Define URL Components
        self.localhost_ip = client_utils.get_localhost_name_ip()
        ib_gateway_host = r"https://" + self.localhost_ip
        ib_gateway_port = r"5000"
        self.ib_gateway_path = ib_gateway_host + ":" + ib_gateway_port
        self.backup_gateway_path = r"https://cdcdyn.interactivebrokers.com/portal.proxy"
        self.login_gateway_path = self.ib_gateway_path + "/sso/Login?forwardTo=22&RL=1&ip2loc=on"

    def _headers(self, mode: str = 'json') -> Dict:
        """Builds the headers.

        Returns a dictionary of default HTTP headers for calls to Interactive
        Brokers API, in the headers we defined the Authorization and access
        token.

        Arguments:
        ----
        mode {str} -- Defines the content-type for the headers dictionary.
            default is 'json'. Possible values are ['json','form']

        Returns:
        ----
        Dict
        """
        headers = None
        if mode == 'json':
            headers = {
                'Content-Type': 'application/json'
            }
        elif mode == 'form':
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        elif mode == 'none':
            headers = None

        return headers

    def _build_url(self, endpoint: str) -> str:
        """Builds a url for a request.

        Arguments:
        ----
        endpoint {str} -- The URL that needs conversion to a full endpoint URL.

        Returns:
        ----
        {srt} -- A full URL path.
        """

        # otherwise build the URL
        return urllib.parse.unquote(
            urllib.parse.urljoin(
                self.ib_gateway_path,
                self.api_version
            ) + r'portal/' + endpoint
        )

    def _make_request(self, endpoint: str, req_type: str,
                      headers: str = 'json', params: dict = None,
                      json: dict = None) -> Dict:
        """Handles the request to the client.

        Handles all the requests made by the client and correctly organizes
        the information so it is sent correctly. Additionally it will also
        build the URL.

        Arguments:
        ----
        endpoint {str} -- The endpoint we wish to request.

        req_type {str} --  Defines the type of request to be made. Can be one of four
            possible values ['GET','POST','DELETE','PUT']

        params {dict} -- Any arguments that are to be sent along in the request. That
            could be parameters of a 'GET' request, or a data payload of a
            'POST' request.

        Returns:
        ----
        {Dict} -- A response dictionary.

        """
        # First build the url.
        url = self._build_url(endpoint=endpoint)

        # Define the headers.
        headers = self._headers(mode=headers)

        # Make the request.
        if req_type == 'POST':
            response = requests.post(url=url, headers=headers, params=params, json=json, verify=False)
        elif req_type == 'GET':
            response = requests.get(url=url, headers=headers, params=params, json=json, verify=False)
        elif req_type == 'DELETE':
            response = requests.delete(url=url, headers=headers, params=params, json=json, verify=False)

        # grab the status code
        status_code = response.status_code

        # grab the response headers.
        response_headers = response.headers

        # Check to see if it was successful
        if response.ok:

            if response_headers.get('Content-Type', 'null') == 'application/json;charset=utf-8':
                data = response.json()
            else:
                data = response.json()

            # Log it.
            logging.debug('''
            Response Text: {resp_text}
            Response URL: {resp_url}
            Response Code: {resp_code}
            Response JSON: {resp_json}
            Response Headers: {resp_headers}
            '''.format(
                resp_text=response.text,
                resp_url=response.url,
                resp_code=status_code,
                resp_json=data,
                resp_headers=response_headers
            )
            )

            return data

        # if it was a bad request print it out.
        elif not response.ok and url != 'https://' + self.localhost_ip + ':5000/v1/portal/iserver/account':
            print(url)
            raise requests.HTTPError()
