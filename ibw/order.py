import logging
from typing import Dict
from typing import List

import ibw.client_utils as client_utils

logging.basicConfig(
    filename='app.log',
    format='%(levelname)s - %(name)s - %(message)s',
    level=logging.DEBUG
)


class IBOrder:

    def __init__(self) -> None:
        self.api_version = 'v1/'

        # Define URL Components
        self.localhost_ip = client_utils.get_localhost_name_ip()
        ib_gateway_host = r"https://" + self.localhost_ip
        ib_gateway_port = r"5000"
        self.ib_gateway_path = ib_gateway_host + ":" + ib_gateway_port
        self.backup_gateway_path = r"https://cdcdyn.interactivebrokers.com/portal.proxy"
        self.login_gateway_path = self.ib_gateway_path + "/sso/Login?forwardTo=22&RL=1&ip2loc=on"

    def get_live_orders(self):
        """
            The end-point is meant to be used in polling mode, e.g. requesting every 
            x seconds. The response will contain two objects, one is notification, the 
            other is orders. Orders is the list of orders (cancelled, filled, submitted) 
            with activity in the current day. Notifications contains information about 
            execute orders as they happen, see status field.
        """

        # define request components
        endpoint = r'iserver/account/orders'
        req_type = 'GET'
        content = client_utils._make_request(
            endpoint=endpoint,
            req_type=req_type,
            localhost_ip=self.localhost_ip,
            ib_gateway_path=self.ib_gateway_path,
            api_version=self.api_version
        )

        return content

    def place_order(self, account_id: str, order: dict) -> Dict:
        """
            Please note here, sometimes this end-point alone can't make sure you submit the order 
            successfully, you could receive some questions in the response, you have to to answer 
            them in order to submit the order successfully. You can use "/iserver/reply/{replyid}" 
            end-point to answer questions.

            NAME: account_id
            DESC: The account ID you wish to place an order for.
            TYPE: String

            NAME: order
            DESC: Either an IBOrder object or a dictionary with the specified payload.
            TYPE: IBOrder or Dict
        """

        if type(order) is dict:
            order = order
        else:
            order = order.create_order()

        # define request components
        endpoint = r'iserver/account/{}/order'.format(account_id)
        req_type = 'POST'
        content = client_utils._make_request(
            endpoint=endpoint,
            req_type=req_type,
            localhost_ip=self.localhost_ip,
            ib_gateway_path=self.ib_gateway_path,
            api_version=self.api_version,
            json=order
        )

        return content

    def place_orders(self, account_id: str, orders: List[Dict]) -> Dict:
        """
            An extension of the `place_order` endpoint but allows for a list of orders. Those orders may be
            either a list of dictionary objects or a list of IBOrder objects.

            NAME: account_id
            DESC: The account ID you wish to place an order for.
            TYPE: String

            NAME: orders
            DESC: Either a list of IBOrder objects or a list of dictionaries with the specified payload.
            TYPE: List<IBOrder Object> or List<Dictionary>
        """

        # EXTENDED THIS
        if type(orders) is list:
            orders = orders
        else:
            orders = orders

        # define request components
        endpoint = r'iserver/account/{}/orders'.format(account_id)
        req_type = 'POST'
        content = client_utils._make_request(
            endpoint=endpoint,
            req_type=req_type,
            localhost_ip=self.localhost_ip,
            ib_gateway_path=self.ib_gateway_path,
            api_version=self.api_version,
            json=orders
        )

        return content

    def place_order_scenario(self, account_id: str, order: dict) -> Dict:
        """
            This end-point allows you to preview order without actually submitting the 
            order and you can get commission information in the response.

            NAME: account_id
            DESC: The account ID you wish to place an order for.
            TYPE: String

            NAME: order
            DESC: Either an IBOrder object or a dictionary with the specified payload.
            TYPE: IBOrder or Dict
        """

        if type(order) is dict:
            order = order
        else:
            order = order.create_order()

        # define request components
        endpoint = r'iserver/account/{}/order/whatif'.format(account_id)
        req_type = 'POST'
        content = client_utils._make_request(
            endpoint=endpoint,
            req_type=req_type,
            localhost_ip=self.localhost_ip,
            ib_gateway_path=self.ib_gateway_path,
            api_version=self.api_version,
            json=order
        )

        return content

    def place_order_reply(self, reply_id: str = None, reply: str = None):
        """
            An extension of the `place_order` endpoint but allows for a list of orders. Those orders may be
            either a list of dictionary objects or a list of IBOrder objects.

            NAME: account_id
            DESC: The account ID you wish to place an order for.
            TYPE: String

            NAME: orders
            DESC: Either a list of IBOrder objects or a list of dictionaries with the specified payload.
            TYPE: List<IBOrder Object> or List<Dictionary>
        """

        # define request components
        endpoint = r'iserver/reply/{}'.format(reply_id)
        req_type = 'POST'
        reply = {
            'confirmed': reply
        }

        content = client_utils._make_request(
            endpoint=endpoint,
            req_type=req_type,
            localhost_ip=self.localhost_ip,
            ib_gateway_path=self.ib_gateway_path,
            api_version=self.api_version,
            json=reply
        )

        return content

    def modify_order(self, account_id: str, customer_order_id: str, order: dict) -> Dict:
        """
            Modifies an open order. The /iserver/accounts endpoint must first
            be called.

            NAME: account_id
            DESC: The account ID you wish to place an order for.
            TYPE: String

            NAME: customer_order_id
            DESC: The customer order ID for the order you wish to MODIFY.
            TYPE: String

            NAME: order
            DESC: Either an IBOrder object or a dictionary with the specified payload.
            TYPE: IBOrder or Dict
        """

        if type(order) is dict:
            order = order
        else:
            order = order.create_order()

        # define request components
        endpoint = r'iserver/account/{}/order/{}'.format(
            account_id, customer_order_id)
        req_type = 'POST'
        content = client_utils._make_request(
            endpoint=endpoint,
            req_type=req_type,
            localhost_ip=self.localhost_ip,
            ib_gateway_path=self.ib_gateway_path,
            api_version=self.api_version,
            json=order
        )

        return content

    def delete_order(self, account_id: str, customer_order_id: str) -> Dict:
        """Deletes the order specified by the customer order ID.

        NAME: account_id
        DESC: The account ID you wish to place an order for.
        TYPE: String

        NAME: customer_order_id
        DESC: The customer order ID for the order you wish to DELETE.
        TYPE: String
        """

        # define request components
        endpoint = r'iserver/account/{}/order/{}'.format(
            account_id, customer_order_id)
        req_type = 'DELETE'
        content = client_utils._make_request(
            endpoint=endpoint,
            req_type=req_type,
            localhost_ip=self.localhost_ip,
            ib_gateway_path=self.ib_gateway_path,
            api_version=self.api_version,
        )

        return content
