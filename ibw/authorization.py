import logging
import pathlib
import socket
import subprocess
import sys
import textwrap
from typing import Dict

import client_utils
from ibw.clientportal import ClientPortal

logging.basicConfig(
    filename='app.log',
    format='%(levelname)s - %(name)s - %(message)s',
    level=logging.DEBUG
)


def get_localhost_name_ip():
    return socket.gethostbyname(socket.gethostname() + '.local')


class IBClient:

    def __init__(self, username: str, account: str, client_gateway_path: str = None) -> None:
        """Initalizes a new instance of the IBClient Object.

        Arguments:
        ----
        username {str} -- Your IB account username for either your paper or regular account.

        account {str} -- Your IB account number for either your paper or regular account.

        Keyword Arguments:
        ----
        password {str} -- Your IB account password for either your paper or regular account. (default:{""})

        Usage:
        ----
            >>> ib_paper_session = IBClient(
                username='IB_PAPER_USERNAME',
                account='IB_PAPER_ACCOUNT',
            )
            >>> ib_paper_session
            >>> ib_regular_session = IBClient(
                username='IB_REGULAR_USERNAME',
                account='IB_REGULAR_ACCOUNT',
            )
            >>> ib_regular_session
        """

        self.account = account
        self.username = username
        self.client_portal_client = ClientPortal()

        self.api_version = 'v1/'
        self._operating_system = sys.platform
        self.session_state_path: pathlib.Path = pathlib.Path(__file__).parent.joinpath('server_session.json').resolve()
        self.authenticated = False
        self.server_process = None

        # Define URL Components
        self.localhost_ip = get_localhost_name_ip()
        ib_gateway_host = r"https://" + self.localhost_ip
        ib_gateway_port = r"5000"
        self.ib_gateway_path = ib_gateway_host + ":" + ib_gateway_port
        self.backup_gateway_path = r"https://cdcdyn.interactivebrokers.com/portal.proxy"
        self.login_gateway_path = self.ib_gateway_path + "/sso/Login?forwardTo=22&RL=1&ip2loc=on"

        if client_gateway_path is None:

            # Grab the Client Portal Path.
            self.client_portal_folder: pathlib.Path = pathlib.Path(__file__).parents[1].joinpath(
                'resources/clientportal.beta.gw'
            ).resolve()

            # See if it exists.
            if not self.client_portal_folder.exists():
                print("The Client Portal Gateway doesn't exist. You need to download it before using the Library.")

        else:

            self.client_portal_folder = client_gateway_path

            # Log the initial Info.
        logging.info(textwrap.dedent('''
	    =================
	    Initialize Client:
	    =================
	    Server Process: {serv_proc}
	    Operating System: {op_sys}
	    Session State Path: {state_path}
	    Client Portal Folder: {client_path}
	    ''').format(
            serv_proc=self.server_process,
            op_sys=self._operating_system,
            state_path=self.session_state_path,
            client_path=self.client_portal_folder
        )
        )

    def create_session(self, set_server=True) -> bool:
        """Creates a new session.

        Creates a new session with Interactive Broker using the credentials
        passed through when the Robot was initalized.

        Usage:
        ----
            >>> ib_client = IBClient(
                username='IB_PAPER_username',
                password='IB_PAPER_PASSWORD',
                account='IB_PAPER_account',
            )
            >>> server_response = ib_client.create_session()
            >>> server_response
                True

        Returns:
        ----
        bool -- True if the session was created, False if wasn't created.
        """

        if set_server:
            self.connect(start_server=True, check_user_input=True)
        else:
            self.connect(start_server=True, check_user_input=False)
            return True

        # then make sure the server is updated.
        if self._set_server():
            return True

        # Try and authenticate.
        auth_response = self.is_authenticated()

        # Log the initial Info.
        logging.info(textwrap.dedent('''
        =================
        Create Session:
        =================
        Auth Response: {auth_resp}
        ''').format(
            auth_resp=auth_response,
        )
        )

        # Finally make sure we are authenticated.
        if 'authenticated' in auth_response.keys() and auth_response['authenticated'] and self._set_server():
            self.authenticated = True
            return True
        else:
            # In this case don't connect, but prompt the user to log in again.
            self.connect(start_server=False)

            if self._set_server():
                self.authenticated = True
                return True

    def _start_server(self) -> str:
        """Starts the Server.
        Returns:
        ----
        str: The Server Process ID.
        """

        IB_WEB_API_PROC = ["sh", r"bin/run.sh", r"root/conf.yaml"]
        self.server_process = subprocess.Popen(
            args=IB_WEB_API_PROC,
            cwd=self.client_portal_folder
        ).pid

        return str(self.server_process)

    def _set_server(self) -> bool:
        """Sets the server info for the session.

        Sets the Server for the session, and if the server cannot be set then
        script will halt. Otherwise will return True to continue on in the script.

        Returns:
        ----
        bool -- True if the server was set, False if wasn't
        """
        success = '\nNew session has been created and authenticated. Requests will not be limited.\n'.upper()
        failure = '\nCould not create a new session that was authenticated, exiting script.\n'.upper()

        # Grab the Server accounts.
        server_account_content = self.server_accounts()

        # Try to do the quick way.
        if server_account_content and 'accounts' in server_account_content:
            accounts = server_account_content['accounts']
            if self.account in accounts:
                # Log the response.
                logging.debug(textwrap.dedent('''
                =================
                Set Server:
                =================
                Server Response: {serv_resp}
                ''').format(
                    serv_resp=server_account_content
                )
                )

                print(success)
                return True
        else:
            print(failure)
            return False

    def connect(self, start_server: bool = True, check_user_input: bool = True) -> bool:
        """Connects the session with the API.

        Connects the session to the Interactive Broker API by, starting up the Client Portal Gateway,
        prompting the user to log in and then returns the results back to the `create_session` method.

        Arguments:
        ----
        start_server {bool} -- True if the server isn't running but needs to be started, False if it
            is running and just needs to be authenticated.

        Returns:
        ----
        bool -- `True` if it was connected.
        """

        logging.debug('Running Client Folder at: {file_path}'.format(
            file_path=self.client_portal_folder))

        print('PID: ', self._start_server())

        # Display prompt if needed.
        if check_user_input:

            print(textwrap.dedent("""{lin_brk}
            The Interactive Broker server is currently starting up, so we can authenticate your session.
                STEP 1: GO TO THE FOLLOWING URL: {url}
                STEP 2: LOGIN TO YOUR account WITH YOUR username AND PASSWORD.
                STEP 3: WHEN YOU SEE `Client login succeeds` RETURN BACK TO THE TERMINAL AND TYPE `ENTER` TO CHECK IF THE SESSION IS AUTHENTICATED.
            {lin_brk}""".format(
                lin_brk='-' * 80,
                url=self.login_gateway_path
            )
            )
            )
            user_input = input(
                'Would you like to make an authenticated request (Press ENTER)? '
            ).upper()

            # Check the auth status
            auth_status = self._check_authentication_user_input()

        else:

            auth_status = True

        return auth_status

    def _check_authentication_user_input(self) -> bool:
        """Used to check the authentication of the Server.

        Returns:
        ----
        bool: `True` if authenticated, `False` otherwise.
        """

        max_retries = 0
        while (max_retries > 4 or self.authenticated == False):

            if max_retries > 10:
                print("Connect failed.")
                sys.exit()

            auth_response = self.is_authenticated(check=True)

            # Log the Auth Response.
            logging.debug('Check User Auth Inital: {auth_resp}'.format(
                auth_resp=auth_response
            )
            )

            if 'statusCode' in auth_response.keys() and auth_response['statusCode'] == 401:
                print("Session isn't connected, closing script.")
                sys.exit()

            elif 'authenticated' in auth_response.keys() and auth_response['authenticated'] == True:
                self.authenticated = True
                break

            elif 'authenticated' in auth_response.keys() and auth_response['authenticated'] == False:
                valid_resp = self.validate()
                reauth_resp = self.reauthenticate()
                auth_response = self.is_authenticated()
                print('valid_resp: ', valid_resp)
                print('reauth: ', reauth_resp)
                print('auth_response: ', auth_response)
                try:
                    serv_resp = self.server_accounts()
                    if 'accounts' in serv_resp:
                        self.authenticated = True

                        # Log the response.
                        logging.debug('Had to do Server Account Request: {auth_resp}'.format(
                            auth_resp=serv_resp
                        )
                        )
                        break
                except:
                    pass

                logging.debug(
                    '''
                    Validate Response: {valid_resp}
                    Reauth Response: {reauth_resp}
                    '''.format(
                        valid_resp=valid_resp,
                        reauth_resp=reauth_resp
                    )
                )

            max_retries += 1

        return self.authenticated

    def is_authenticated(self, check: bool = False) -> Dict:
        """Checks if session is authenticated.

        Overview:
        ----
        Current Authentication status to the Brokerage system. Market Data and 
        Trading is not possible if not authenticated, e.g. authenticated 
        shows `False`.

        Returns:
        ----
        (dict): A dictionary with an authentication flag.   
        """

        # define request components
        endpoint = 'iserver/auth/status'

        if not check:
            req_type = 'POST'
        else:
            req_type = 'GET'

        content = client_utils._make_request(
            endpoint=endpoint,
            req_type=req_type,
            headers='none',
            localhost_ip=self.localhost_ip,
            ib_gateway_path=self.ib_gateway_path,
            api_version=self.api_version
        )

        return content

    def reauthenticate(self) -> Dict:
        """Reauthenticates an existing session.

        Overview:
        ----
        Provides a way to reauthenticate to the Brokerage 
        system as long as there is a valid SSO session, 
        see /sso/validate.

        Returns:
        ----
        (dict): A reauthentication response.        
        """

        # Define request components.
        endpoint = r'iserver/reauthenticate'
        req_type = 'POST'

        # Make the request.
        content = client_utils._make_request(
            endpoint=endpoint,
            req_type=req_type,
            localhost_ip=self.localhost_ip,
            ib_gateway_path=self.ib_gateway_path,
            api_version=self.api_version
        )

        return content

    def validate(self) -> Dict:
        """Validates the current session for the SSO user."""

        # define request components
        endpoint = r'sso/validate'
        req_type = 'GET'
        content = client_utils._make_request(
            endpoint=endpoint,
            req_type=req_type,
            localhost_ip=self.localhost_ip,
            ib_gateway_path=self.ib_gateway_path,
            api_version=self.api_version
        )

        return content

    def server_accounts(self):
        """
            Returns a list of accounts the user has trading access to, their
            respective aliases and the currently selected account. Note this
            endpoint must be called before modifying an order or querying
            open orders.
        """

        # define request components
        endpoint = 'iserver/accounts'
        req_type = 'GET'
        content = client_utils._make_request(
            endpoint=endpoint,
            req_type=req_type,
            localhost_ip=self.localhost_ip,
            ib_gateway_path=self.ib_gateway_path,
            api_version=self.api_version
        )

        return content
