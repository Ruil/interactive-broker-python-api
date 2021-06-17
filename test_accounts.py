import ibw.accounts as accounts


my_accounts = accounts.IBAccounts()
print(my_accounts.server_accounts())

print(my_accounts.portfolio_accounts())

print(my_accounts.portfolio_positions('U5531042'))
