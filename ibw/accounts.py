from typing import Dict

import client_base


class IBAccounts(client_base.IBBase):

    def __init__(self) -> None:
        super().__init__()

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
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
        )

        return content

    def portfolio_accounts(self):
        """
            In non-tiered account structures, returns a list of accounts for which the 
            user can view position and account information. This endpoint must be called prior 
            to calling other /portfolio endpoints for those accounts. For querying a list of accounts 
            which the user can trade, see /iserver/accounts. For a list of subaccounts in tiered account 
            structures (e.g. financial advisor or ibroker accounts) see /portfolio/subaccounts.

        """

        # define request components
        endpoint = 'portfolio/accounts'
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
        )

        return content

    def portfolio_sub_accounts(self):
        """
            Used in tiered account structures (such as financial advisor and ibroker accounts) to return a 
            list of sub-accounts for which the user can view position and account-related information. This 
            endpoint must be called prior to calling other /portfolio endpoints for those subaccounts. To 
            query a list of accounts the user can trade, see /iserver/accounts.

        """

        # define request components
        endpoint = r'​portfolio/subaccounts'
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
        )

        return content

    def portfolio_account_info(self, account_id: str) -> Dict:
        """
            Used in tiered account structures (such as financial advisor and ibroker accounts) to return a 
            list of sub-accounts for which the user can view position and account-related information. This 
            endpoint must be called prior to calling other /portfolio endpoints for those subaccounts. To 
            query a list of accounts the user can trade, see /iserver/accounts.

            NAME: account_id
            DESC: The account ID you wish to return info for.
            TYPE: String
        """

        # define request components
        endpoint = r'portfolio/{}/meta'.format(account_id)
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
        )

        return content

    def portfolio_account_summary(self, account_id: str) -> Dict:
        """
            Returns information about margin, cash balances and other information 
            related to specified account. See also /portfolio/{accountId}/ledger. 
            /portfolio/accounts or /portfolio/subaccounts must be called 
            prior to this endpoint.

            NAME: account_id
            DESC: The account ID you wish to return info for.
            TYPE: String
        """

        # define request components
        endpoint = r'portfolio/{}/summary'.format(account_id)
        req_type = 'GET'
        content = self._make_request(endpoint=endpoint, req_type=req_type, )

        return content

    def portfolio_account_ledger(self, account_id: str) -> Dict:
        """
            Information regarding settled cash, cash balances, etc. in the account's 
            base currency and any other cash balances hold in other currencies. /portfolio/accounts 
            or /portfolio/subaccounts must be called prior to this endpoint. The list of supported 
            currencies is available at https://www.interactivebrokers.com/en/index.php?f=3185.

            NAME: account_id
            DESC: The account ID you wish to return info for.
            TYPE: String
        """

        # define request components
        endpoint = r'portfolio/{}/ledger'.format(account_id)
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
        )

        return content

    def portfolio_account_positions(self, account_id: str, page_id: int = 0) -> Dict:
        """
            Returns a list of positions for the given account. The endpoint supports paging, 
            page's default size is 30 positions. /portfolio/accounts or /portfolio/subaccounts 
            must be called prior to this endpoint.

            NAME: account_id
            DESC: The account ID you wish to return positions for.
            TYPE: String

            NAME: page_id
            DESC: The page you wish to return if there are more than 1. The
                  default value is `0`.
            TYPE: String

            ADDITIONAL ARGUMENTS NEED TO BE ADDED!!!!!
        """

        # define request components
        endpoint = r'portfolio/{}/positions/{}'.format(account_id, page_id)
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
        )

        return content

    def portfolio_account_position(self, account_id: str, conid: str) -> Dict:
        """
            Returns a list of all positions matching the conid. For portfolio models the conid 
            could be in more than one model, returning an array with the name of the model it 
            belongs to. /portfolio/accounts or /portfolio/subaccounts must be called prior to 
            this endpoint.

            NAME: account_id
            DESC: The account ID you wish to return positions for.
            TYPE: String

            NAME: conid
            DESC: The contract ID you wish to find matching positions for.
            TYPE: String
        """

        # Define request components.
        endpoint = r'portfolio/{}/position/{}'.format(account_id, conid)
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
        )

        return content

    def portfolio_positions(self, conid: str) -> Dict:
        """
            Returns an object of all positions matching the conid for all the selected accounts. 
            For portfolio models the conid could be in more than one model, returning an array 
            with the name of the model it belongs to. /portfolio/accounts or /portfolio/subaccounts 
            must be called prior to this endpoint.

            NAME: conid
            DESC: The contract ID you wish to find matching positions for.
            TYPE: String          
        """

        # Define request components.
        endpoint = r'portfolio/positions/{}'.format(conid)
        req_type = 'GET'
        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
        )

        return content
