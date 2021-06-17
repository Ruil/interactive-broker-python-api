import ibw.client_base as client_base


my_client = client_base.IBBase()
print(my_client.symbol_search('FB'))

print(my_client.symbol_search('TNA'))
