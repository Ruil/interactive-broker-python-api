import datetime
import pathlib
import sched
import time

from ibw.client import IBClient
from configparser import ConfigParser

MARKET_CLOSE = datetime.time(16, 0)
RENEW_DELAY = 60
PRIORITY = 1

# Grab configuration values.
config = ConfigParser()
file_path = pathlib.Path('../ib_client/config.ini').resolve()
config.read(file_path)

# Load the details.
account = config.get('main', 'REGULAR_ACCOUNT')
username = config.get('main', 'REGULAR_USERNAME')

print(account)
print(aa)

# Create a new session of the IB Web API.
ib_client = IBClient(
    username=paper_username,
    account=paper_account,
    is_server_running=True
)

# create a new session
ib_client.create_session()


def renew_session(scheduler):
    if datetime.datetime.now().time() >= MARKET_CLOSE:
        print('Market is closed, exit.')
        return

    valid_resp = ib_client.validate()
    reauth_resp = ib_client.reauthenticate()
    auth_response = ib_client.is_authenticated()
    print(
        '''
        Validate Response: {valid_resp}
        Reauth Response: {reauth_resp}
        '''.format(
            valid_resp=valid_resp,
            reauth_resp=reauth_resp
        )
    )

    print('scheduled next run in: ', RENEW_DELAY, ' s')
    scheduler.enter(
        RENEW_DELAY,
        renew_session,
        scheduler)


scheduler = sched.scheduler(time.time, time.sleep)

print('scheduled next run in: ', RENEW_DELAY, ' minutes')
scheduler.enter(
    RENEW_DELAY,
    PRIORITY,
    renew_session,
    scheduler)

scheduler.run()
