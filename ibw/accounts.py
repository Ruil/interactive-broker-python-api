import logging

logging.basicConfig(
    filename='app.log',
    format='%(levelname)s - %(name)s - %(message)s',
    level=logging.DEBUG
)

class IBAccounts:

    def __init__(client_gateway_path: str = None) -> None:
    
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
