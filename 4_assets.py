## reset_.bat && start_.bat

from myutil import *
# prepare_addrs()
addrs = load_addrs()
# print_js(addrs)  
## set_addrs.bat

''' Get Address Balance:
      multichain-cli chain1 getaddressbalances <addr>

Initially all addresses, include 'root' have zero balances.
mc getaddressbalances %addr0%
'''
def get_balance(addr):
    bs = api.getaddressbalances(addr)
    if bs == []:
        print(addr, 0)
    else:
        for b in bs:
            print(b['name'], b['qty'])
# get_balance(addrs[1])

''' List addresses that have 'perms' permissions.
'perms' is a str of permissions separated by ','.
Initially the 'root' address has all permissions, others have none.
An address must have 'receive,send' permissions to send and receive assets. 
'''
def list_permissions(perms):  
    for j in api.listpermissions(perms, addrs):
        print(j['address'], j['type'])	
# list_permissions('receive,send')

## Grant 'receive,send' permission to all addresses except 'root'.
def grant_perm():
    a = ','.join(addrs[1:]) ## a str of addresses separated by ','.
    api.grant(a, 'receive,send')	
# grant_perm()
#---------------------------------------------------------

''' Assets: are tokens.
To List Assets:
      multichain-cli chain1 listassets
## mc listassets
Initially there is no assets.
'''
def list_assets():
    assets = api.listassets()
    if assets == []:
        print('None.') 
    else:
        for a in assets:
            print(a['name'] , a['issueqty'])
# list_assets()         

''' Issue: is a process of creating new or more assets.
To create an asset and assign to an address
     multichain-cli chain1 issue <addr> <asset> <amount> <subdivide>
     multichain-cli chain1 issuefrom <from_addr> <to_addr> <asset> <amount> <subdivide>
For 'issue', 'root' is the issuer by default.
The issuer may be 'root' or has 'admin' and 'issue' permission.
The receiver must have 'receive' permission.
<subdivide> is the smallest unit. 
If success, return the 'txid' that issues the asset.
A 'close' asset cannot be issued more than once, it is the default.
An address may own more than one assets.
'root' may have no balances but can issue assets to any addresses.
Normally we start with 'root' issuses an asset to itself.
'issue' and 'issuefrom' may include metadata e.g. {"country":"TH","type":"demo"}

Ex. 'addr0'(root) issues 'as0' asset for 100 units to itself with subdivide 0.01.
## mc issue %addr0% as0 100 0.01
## mc getaddressbalances %addr0%
'''
def issue(recv, asset, amount, subd=1):
    print(api.issue(recv, asset, amount, subd))

## Ex. Root issues 'as1' asset for 1000 units to addr1 with subdivide 1.
# issue(addrs[1], 'as1', 1000, 1)
# list_assets()
# get_balance(addrs[1])

''' To get Asset Info:
      multichain-cli chain1 getassetinfo <asset> <versbose>=false

'versbose' is a boolen for requests more information.
'name' and 'issueqty' are the name and amount of the asset.
## mc getassetinfo as0
## mc getassetinfo as1 true
----------------------------------------------------

'open' asset: is the asset that can be reissued (more than once).
An asset may be expressed as a string or a json.
An 'open' asset must be described as json, with 'open' is true.
  multichain-cli chain1 issue <recv> "{\"name\":<asset_name>, \"open\": true }" <amount> <subdivide>
  multichain-cli chain1 issueform <form_addr> <to_addr> "{\"name\":<asset_name>, \"open\": true }" <amount> <subdivide>

Ex. Issue 'ax' asset for 100 to addr1 as an opened asset:
## mc issue %addr1% "{\"name\":\"ax\", \"open\":true}" 100 1
## mc getassetinfo ax

To issuing more asset:
     multichain-cli chain1 issuemore <recv> <asset> <amount>
     multichain-cli chain1 issuemoreform <form_addr> <to_addr> <asset> <amount>
## mc issuemore %addr1% ax 200
## mc getaddressbalances %addr1%
'''
#-------------------------------------------------------

''' Send Asset:
     multichain-cli chain1 sendasset <addr> <asset> <amount>

The sender is 'root' or 'admin' by default.
The sender must have enough asset and 'send' premissions.
<addr> is address of the receiver and must has 'receive' permission.
If success, return 'txid' that send the asset.
Multichain handles the balances for both sender and receiver.
The wallet take cares of creating and signing tx.
## mc getaddressbalances %addr0%
## mc getaddressbalances %addr1%
## mc sendasset %addr1% as0 10		## addr0 is the sender.
## mc getaddressbalances %addr0%
## mc getaddressbalances %addr1%
'''
def send_asset(recv, asset, amount):
    print(api.sendasset(recv, asset, amount))

## Ex. addr0 send 'as1' asset for 10 units to addr1.
send_asset(addrs[1], 'as1', 10)

''' To send asset from non-root:
Senders must has 'send' permission. Receiver must has 'receive' permission.
   multichain-cli chain1 sendassetfrom <from_addr> <to_addr> <asset> <amount>
## mc getaddressbalances %addr1%
## mc getaddressbalances %addr2%
## mc sendassetfrom %addr1% %addr2% as0 5
## mc getaddressbalances %addr1%
## mc getaddressbalances %addr2%
'''
def send_asset_form(from_addr, to_addr, asset, amount):
    print(api.sendassetfrom(from_addr, to_addr, asset, amount))

## Ex. addr1 sends 'as0' asset for 5 units to addr2.
# send_asset_form(addrs[1], addrs[2], 'as0', 5)

''' To send multiple assets in a tx. 
The asset is represnted as json:
        {<asset1>:<amount1>, <asset2>:<amount2>, ...}
    multichain-cli chain1 send <receiver_addr> <json>
    multichain-cli chain1 sendfrom <from_addr> <to_addr> <json>

Ex. addr1 sends 'as1' for 1 units and 'as2' for 2 units to addr2.
## mc sendfrom %addr1% %addr2% "{\"as1\":1, \"as2\":2}"
'''
#----------------------------------------------------

## converting: string <--> hex string  (defined in myutil.py)
# print(str_hex('Hello'))         ## 48656c6c6f
# print(hex_str('48656c6c6f'))    ## Hello
#----------------------------------------------------

''' Assets may have metadata.
The asset must be represented as json.
		{<asset name>: <amount>}

To send asset with metadata:
  multichain-cli chain1 sendwithdata <to_addr> <json_asset> <metadata>
  multichain-cli chain1 sendwithdatafrom <from_addr> <to_addr> <json_asset> <metadata>

If <metadata> is just a text it must be a hex-string:
Ex. addr0 sends 'as0' for 1 units to addr1 with metadata 'Hello'.
## mc sendwithdata %addr1% "{\"as0\":1}" 48656c6c6f
'''
def sendfrom_md(sender, recv, json_asset, md):
    print(api.sendwithdatafrom(sender, recv, json_asset, md))
## Ex. addr1 sends 'as1' for 1 units to addr2 with metadata 'Hi'.
# sendfrom_md(addrs[1], addrs[2], {'as1': 1}, str_hex('Hi'))

''' To list the last <n> transactions of an <addr>:
      multichain-cli chain1 listaddresstransactions <addr> <n>
'''
## mc listaddresstransactions %addr2% 2

## The metadata is stored in 'data' of the tx.
def read_data(addr, n):   ## n is the number of tx.
    for t in api.listaddresstransactions(addr, n):
        d = t['data'][0]
        if type(d) == str:
            print(hex_str(d))
        else:
            print(d)
# read_data(addrs[2], 1)
#---------------------------------------------------

''' Sending Asset with Text Metadata:'
The asset must be represented as json.
<metadata> may be a json in the form of:  {"text": "<str>"}
## mc sendwithdatafrom %addr0% %addr1% {\"as0\":1} "{\"text\": \"Hello!\"}"
'''
# sendfrom_md(addrs[0], addrs[1], {'as1': 1}, {"text": "Hi how are you?"})
# read_data(addrs[1], 1)

''' <metadata> may be a json of the form:  {"json": {"id":"123", "name":"john"}}
## mc sendwithdatafrom %addr0% %addr1% "{\"as1\":1}" "{\"json\": {\"id\":\"123\", \"name\":\"john\"}}"
'''
def send_jsonobj():
    send_with_datafrom(addrs[0], addrs[1], {'as1': 1}, 
                                      {"json": [{'id': 500, 'name': 'jack'},
                                      {'id': 600, 'name': 'joe'}] })
# send_jsonobj()
# read_data(addrs[1], 1)
