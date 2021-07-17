import ibw.accounts as accounts

my_accounts = accounts.IBAccounts()
print('server_accounts: ', my_accounts.server_accounts())

print('portfolio_accounts: ', my_accounts.portfolio_accounts())

print('Position is: ', my_accounts.portfolio_positions('73340487'))


