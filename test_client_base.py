import ibw.client_base as client_base


def get_conid(respond):
    return respond[0]['conid']
        
my_client = client_base.IBBase()
print(my_client.symbol_search('FB'))

print(my_client.symbol_search('SOXL'))

response = my_client.symbol_search('TNA')
print(response)
print(get_conid(response))


