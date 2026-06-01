## reset_.bat && start_.bat

from myutil import *
# prepare_addrs()
addrs = load_addrs()
# print_js(addrs)  
## set_addrs.bat

## Grant 'receive,send' permissions to 3 addresses.
def prepare_perm():
    a = '{},{},{}'.format(addrs[1], addrs[2], addrs[3])
    api.grant(a, 'receive,send')
    for j in api.listpermissions('receive,send', a):
        print(j['address'], j['type'])
# prepare_perm()
#---------------------------------------------------------

''' Streams are storages of items of the from 'name':'value'.

To list streams:
        multichain-cli chain1 liststreams
## mc liststreams
Initially there is the 'root' stream, created when the first node is started.
'''
def list_streams():
    for s in api.liststreams():
        print(s['name'])
# list_streams()

''' To create stream:
   multichain-cli chain1 create stream <stream_name> <open>
   multichain-cli chain1 createfrom <from_addr> stream <stream_name> <open>

Ex. Create 's1' stream with 'open' property.
## mc create stream s1 true
The creater must have 'create' permission. e.g. 'root' or 'admin'.
'createfrom' allows <from_addr> to create a stream, but needs 'create' permission.
An 'open' stream allows anyone with 'send' permission to publish to the stream.
If success, return the 'txid' that creates the stream.
'''
# print(api.create('stream', 's2', True))

''' 'create' Permission:
To allow a 'non-root' to create a stream, it must have 'create' permission.
## mc grant %addr1% create
## mc createfrom %addr1% stream s3 false

To get stream info:
      multichain-cli chain1 getstreaminfo <stream_name>
# mc getstreaminfo s1
'''
def get_stream_info(name):
    s = api.getstreaminfo(name)
    # print(s)
    print('name: ', s['name'])
    print('restrict: ', s['restrict'])
# get_stream_info('s1')
# get_stream_info('s3')     ## 'open' streams have 'write'=False.

''' A stream permission is for a particular stream and belong to an address.
To list addresses that have some permissions to a stream:
      multichain-cli chain1 listpermissions <stream_name>.*
mc listpermissions s1.*
The 'root' has 'write' permission to all streams, but not listed.
'''
def list_permissions(sname):
    for j in api.listpermissions(sname+'.*'):
        print(j.get('address'), ': ', j.get('type'))
# list_permissions('s1')
# list_permissions('s3')

''' A stream with 'write' permission allows all addresses to publish to 
 the stream without 'admin' or 'activate' permissions.
When a task or event has been completed, we may need to prevent
 more publish to a stream. So its 'write' permissions should be revokeed.
'''
#-----------------------------------------------------------

## Create sample hex strings.
hello_hex = str_hex('hello');   ## print(hello_hex)  ## 68656c6c6f
hi_hex = str_hex('hi');         ## print(hi_hex)     ## 6869
whatup_hex = str_hex('whatup'); ## print(whatup_hex) ## 776861747570

''' Publish hex string:
A stream item may contain <key>/<value>, where <value> is a hex string.
  multichain-cli chain1 publish <stream_name> <key> <value>
  multichain-cli chain1 publishfrom <from_addr> <stream_name> <key> <value>
Publishing to an open stream requires 'send' permissions.
<key> must be string, <value> may be hex-string or json.
Return the 'txid' that publishs to the stream if success.
More than one items may have the same key.
## mc publish s1 k1 68656c6c6f
## mc publishfrom %addr1% s1 k2 6869
'''
def pub_hex(sname, key, value):
    print(api.publish(sname, key, value))
# pub_hex('s2', 'key1', hello_hex)
# pub_hex('s2', 'key1', hi_hex)
#-----------------------------------------------------------------

''' Reading a stream requires tracking the stream.
To start tracking a stream, the node must subscribe to the stream.
To subscribe to a stream:
     multichain-cli chain1 subscribe <stream_name>
## mc subscribe s1
if success, return nothings.

To list items of a stream:
  multichain-cli chain1 liststreamitems <stream_name>
## mc liststreamitems s1
'''
def list_stream_items(sname):
    for js in api.liststreamitems(sname):
        print(js['keys'], hex_str(js['data']))
# list_stream_items('s1')

''' To list items by Stream and Key:
   multichain-cli chain1 liststreamkeyitems <stream_name> <key>
'''
def list_stream_key_items(sname, key):
    for r in api.liststreamkeyitems(sname, key):
        print(hex_str(r['data']))
# list_stream_key_items('s1', 'k1')
# list_stream_key_items('s1', 'k2')

''' Stream allows duplicated key.
## mc publish s1 dk 68656c6c6f            ## hello
## mc publish s1 dk 776861747570          ## whatup
'''
# list_stream_key_items('s1', 'dk')
## Duplicated keys may be both useful and unwanted.
## Developers must take charge in controlling the policy.

## If there is no duplicate keys, the result can be found at the first item.
def non_duplicate_key(sname, key):
    r = api.liststreamkeyitems(sname, key)
    print(hex_str(r[0].get('data')))
# non_duplicate_key('s1', 'dk')

#--------------------------------------------------------------
''' Publish Text:
<value> must be a json of the form {"text": <txt>}.
        multichain-cli chain1 publish <stream_name> <key> {"text": <txt>}
## mc publish s1 t1, "{\"text\": \"How are you?\"}"
'''
# print(api.publish('s1', 't2', {'text': 'How do you do?'}))

def read_txt(sname, key):
    for j in api.liststreamkeyitems(sname, key):
        d = j['data']
        if type(d) is dict:     ## json
            print(d['text'])
# read_txt('s1', 't1')

''' Publish Json: To simulate table of records.
<value> must be a json of the form {"json": <json>}.
Duplicated keys allows grouping(or table) but <value> should be unique.
    multichain-cli chain1 publish <stream_name> <key> {'json': <json>}
Ex. A record of student with id, name and gpa.
## mc publish s1 kj "{\"json\":{\"id\":\"1\", \"gpa\":\"3.8\", \"name\":\"John\"}}"

Records can be grouped (into a table) by certain key.
Ex. Using 'dep' as the key and student json as the value. '''
def pub_student(sname, dep, id, name, gpa):
    json = {'json': {'id': id, 'name': name, 'gpa': gpa}}
    print(api.publish(sname, dep, json))

def pub_student_test():
    pub_student('s1', 'cs', 1, 'John', 2.1)
    pub_student('s1', 'cs', 2, 'Jack', 3.8)
    pub_student('s1', 'ee', 3, 'Joe', 4.0)
# pub_student_test()

## Read json: We can list items with certain <key>, simular to 'projection'.
def read_student(sname, dep):
    for j in api.liststreamkeyitems(sname, dep):
        student =j['data']['json']
        print(student['id'], student['name'], student['gpa'])
## Ex. To select (projection) students by dep.
# read_student('s1', 'cs')
# read_student('s1', 'ee')

def add_more_students():
    pub_student('s1', 'it', 4, 'Jame', 1.2)
    pub_student('s1', 'cs', 5, 'Jim', 3.1)
    pub_student('s1', 'ce', 6, 'Jody', 2.1)
# add_more_students()
# read_student('s1', 'cs')

## Ex. To find gpa by dep and name.
def get_gpa(sname, dep, name):
    for js in api.liststreamkeyitems(sname, dep):
        s = js['data']['json']
        if s['name'] == name:
            print(s['gpa'])
# get_gpa('s1', 'cs', 'Jack')

################################################################

''' List Item Options:
  multichain-cli chain1 liststreamkeyitems <sname> <key> 
          <verbose>=False, <count>=10, <start>=0
<verbose> if True contains info about tx.
<count> number of items to be listed (from the first).
<start> (from 0 based position), if negative start from the end.
## mc liststreamkeyitems s1 cs
## mc liststreamkeyitems s1 cs true
'''
def list_keyitems(sname, dep, count=10, start=0):
    for j in api.liststreamkeyitems('sname', dep, False, count, start):
        print(j['keys'], j['data'])
# list_keyitems('s1', 'cs')
# list_keyitems('s1', 'ce')
# list_keyitems('s1', 'cs', 2)
# list_keyitems('s1', 'cs', 3, 1)
# list_keyitems('s1', 'cs', 2, 2)
# list_keyitems('s1', 'cs', 1, 0)      ## the first
# list_keyitems('s1', 'cs', 1, -1)     ## the last

''' Key List: List all items by a keys list.
    multichain-cli chain1 liststreamqueryitems <sname> <json>
## mc liststreamqueryitems s1 "{\"keys\":[\"cs\"]}"
<json> defines keys list in the form: {"keys": ["key1", "key2", ...]} 
'''
def list_queryitems(sname, keys):
    for j in api.liststreamqueryitems(sname, keys):
        print(j['keys'], j['data'])
# list_queryitems('s1', {'keys': ['cs']})
# list_queryitems('s1', {'keys': ['it']})
# list_queryitems('s1', {'keys': ['cs', 'it']}) ## no items with the list of keys

## Add more records with key list:
## <key> may be a list of keys.
def pub_items_with_keylist():
    print(api.publish('s1', 'cs', {'json': {'dep': 'Computer Science'}}))
    print(api.publish('s1', ['cs','oo'], {'json':{'dep':'Computer Science','title':'OO Programming'}}))
    print(api.publish('s1', ['cs','oo'], {'json':{'dep':'Computer Science','title':'OO Design and Analysis'}}))
    print(api.publish('s1', ['cs','dm'], {'json':{'dep':'Computer Science','title':'Discrete Math'}}))
    print(api.publish('s1', 'ee', {'text': 'Electrical Engineer'}))
    print(api.publish('s1', ['ee','dm'], {'json':{'dep':'Electrical Engineer','title':'Discrete Math'}}))
# pub_items_with_keylist()

##  Query by Keys List:
def query_keys():
    # for js in api.liststreamkeyitems('s1', 'ee'):
    # for js in api.liststreamqueryitems('s1', {'keys':['cs']}):
    for js in api.liststreamqueryitems('s1', {'keys':['oo', 'cs']}):
    # for js in api.liststreamqueryitems('s1', {'keys':['dm', 'cs']}):
    # for js in api.liststreamqueryitems('s1', {'keys':['ee']}):
    # for js in api.liststreamqueryitems('s1', {'keys':['dm']}):
    # for js in api.liststreamqueryitems('s1', {'keys':['ee','cs']}):  ## not intersect
        print(js['keys'], js['data'])
# query_keys()

