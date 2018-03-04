from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport, TSocket

from project import *
import getpass
import hashlib
import uuid
import json

ip = '192.168.0.12'
#ip = '144.122.71.154'
port = 8081

socket = TSocket.TSocket(ip,port)
transport = TTransport.TFramedTransport(socket)
protocol = TBinaryProtocol.TBinaryProtocol(transport)
client = myService.Client(protocol)
transport.open()

username = raw_input("Login: ")
password = getpass.getpass()

password = hashlib.sha1(password).hexdigest().upper()
mac = hex(uuid.getnode())

result =json.loads( client.login(username, password, mac) )

if result['result'] == myService.LoginResponse.SuccessNewDevice:
    auth_key = result['key']
    cap = {'bluetooth_le': 'NOT FOUND', 'bluetooth_addr': 'NOT FOUND', 'charge': 'NOT FOUND', 'camera': 'NOT FOUND', 'type': 'edison', 'model_name': 'Intel Edison','sensors': ['Temperature', 'Sound', 'Light', 'Led', 'Lcd'] }
    name = "Intel Edison"

    client.addDevice(mac, name, " ", json.dumps(cap), auth_key)

elif result['result'] != myService.LoginResponse.Success:
    print "Failed"
