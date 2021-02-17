from typing import Dict
from typing import List

from . import client_base


class IBMarket(client_base.IBBase):

    def __init__(self) -> None:
        super().__init__()


    def market_data(self, conids: List[str], since: str, fields: List[str]) -> Dict:
        """
            Get Market Data for the given conid(s). The end-point will return by
            default bid, ask, last, change, change pct, close, listing exchange.
            See response fields for a list of available fields that can be request
            via fields argument. The endpoint /iserver/accounts should be called
            prior to /iserver/marketdata/snapshot. To receive all available fields
            the /snapshot endpoint will need to be called several times.

            NAME: conid
            DESC: The list of contract IDs you wish to pull current quotes for.
            TYPE: List<String>

            NAME: since
            DESC: Time period since which updates are required.
                  Uses epoch time with milliseconds.
            TYPE: String

            NAME: fields
            DESC: List of fields you wish to retrieve for each quote.
            TYPE: List<String>
        """

        # define request components
        endpoint = 'iserver/marketdata/snapshot'
        req_type = 'GET'

        # join the two list arguments so they are both a single string.
        conids_joined = self._prepare_arguments_list(parameter_list=conids)

        if fields is not None:
            fields_joined = ",".join(str(n) for n in fields)
        else:
            fields_joined = ""

        # define the parameters
        if since is None:
            params = {
                'conids': conids_joined,
                'fields': fields_joined
            }
        else:
            params = {
                'conids': conids_joined,
                'since': since,
                'fields': fields_joined
            }

        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            params=params
        )

        return content

    def market_data_history(self, conid: str, period: str, bar: str) -> Dict:
        """
            Get history of market Data for the given conid, length of data is controlled by period and
            bar. e.g. 1y period with bar=1w returns 52 data points.

            NAME: conid
            DESC: The contract ID for a given instrument. If you don't know the contract ID use the
                  `search_by_symbol_or_name` endpoint to retrieve it.
            TYPE: String

            NAME: period
            DESC: Specifies the period of look back. For example 1y means looking back 1 year from today.
                  Possible values are ['1d','1w','1m','1y']
            TYPE: String

            NAME: bar
            DESC: Specifies granularity of data. For example, if bar = '1h' the data will be at an hourly level.
                  Possible values are ['5min','1h','1w']
            TYPE: String
        """

        # define request components
        endpoint = 'iserver/marketdata/history'
        req_type = 'GET'
        params = {
            'conid': conid,
            'period': period,
            'bar': bar
        }

        content = self._make_request(
            endpoint=endpoint,
            req_type=req_type,
            params=params
        )

        return content

    @staticmethod
    def _prepare_arguments_list(parameter_list: List[str]) -> str:
        """Prepares the arguments for the request.

        Some endpoints can take multiple values for a parameter, this
        method takes that list and creates a valid string that can be
        used in an API request. The list can have either one index or
        multiple indexes.

        Arguments:
        ----
        parameter_list {List} -- A list of paramater values assigned to an argument.

        Usage:
        ----
            >>> SessionObject._prepare_arguments_list(parameter_list=['MSFT','SQ'])

        Returns:
        ----
        {str} -- The joined list.

        """

        # validate it's a list.
        if type(parameter_list) is list:

            # specify the delimiter and join the list.
            delimiter = ','
            parameter_list = delimiter.join(parameter_list)

        return parameter_list