import sys, glob
sys.path.append('project')

import clientService
import myService
import sqlite3 as lite
import hashlib
import bcrypt
import uuid
import logging


from thrift.transport import TSocket
from thrift.transport import TSSLSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.server import TNonblockingServer

class ServerHandler:
  def __init__(self):
    self.con = lite.connect('db/test.db', check_same_thread=False)
    self.cur = self.con.cursor()
    self.log = {}
    self.setupDb()

  def setupDb(self):
    try:
        self.cur.execute('CREATE TABLE Users(Id INT, Username TEXT Unique, Password TEXT, Name TEXT, email TEXT Unique, primary key(Id))')
        self.cur.execute('CREATE TABLE Devices(UserId INT, DeviceId INT, DeviceName TEXT, DeviceMac TEXT Unique, DeviceIp TEXT, DevicePort TEXT, Status INT, primary key(UserId, DeviceId), foreign key(UserId) references Users(Id) )')
    except Exception as e:
      	print e
      	print "db exists"

  #TODO--- Add Email Exception, Return
  def registerRequest(self, username, password, name, email):
    m = bcrypt.hashpw(password, bcrypt.gensalt())

    print "registerRequest-> " + username + "\t" + name + "\t" + email
    try:
      while 1:
        generatedId = hash(str(uuid.uuid1())) % 100000
        query = ('Select * From Users Where Id=%s' %(generatedId))
        self.cur.execute(query)
        try:
          self.cur.fetchone()[0]
        except:
          break
      query = ('INSERT INTO Users VALUES(%s,"%s", "%s", "%s","%s")' %(generatedId, username, m,name,email) )
      self.cur.execute(query)
    except lite.IntegrityError:
      print "RegisterFail"
      return myService.RegisterResponse.UsernameExists
    except Exception as e:
      print e
      return myService.RegisterResponse.Fail
    print "Register Success with Id -> " + str(generatedId)
    return myService.RegisterResponse.Success


  def login(self, username, password, mac):
    print "login-> " + username + "\t" + mac
    try:
      query =  ('Select Password From Users Where Username="%s"' %(username) )
      self.cur.execute(query)


    except Exception:
      return myService.LoginResponse.Fail

    try:
      ps = self.cur.fetchone()[0]
    except Exception:
      return myService.LoginResponse.WrongInfo

    if bcrypt.hashpw(password, ps.encode('utf-8')) == ps:
      self.cur.execute('Select Id From Users Where Username="%s"' %(username) )
      self.userid = self.cur.fetchone()[0]

      try:
        query = ('Select * From Devices Where UserId=%s and DeviceMac="%s"' %(self.userid, mac))
        self.cur.execute(query)
        self.cur.fetchone()[0]
      except:
        return myService.LoginResponse.SuccessNewDevice
      query = ('Update Devices Set Status=1 Where DeviceMac="%s"' %(mac))
      self.cur.execute(query)
      return myService.LoginResponse.Success
    else:
      return myService.LoginResponse.WrongInfo




  def addDevice(self,mac,name,crt):
      print "addDevice -> " + mac + "\t" + name
      query = ('Select * From Devices Where DeviceMac="%s" and UserId=%s' %(mac,self.userid) )

      print mac + "\t" + str(self.userid) + "\t" + transport.clientaddr[0] + "\t" + str(transport.clientaddr[1])
      print transport.clienttt

      try:
        self.cur.execute(query)
      except Exception as e:
	print e
        return myService.AddDeviceResponse.Fail

      try: #check if query returned empty. If not empty DeviceExists, else device not exists for that user. Add device.
        cid = self.cur.fetchone()[0]
      except:
        while 1:
          generatedId = hash(str(uuid.uuid1())) % 100000
          query = ('Select * From Devices Where DeviceId=%s' %(generatedId))
          self.cur.execute(query)
          try:
            self.cur.fetchone()[0]
          except:
            break
        query = ('INSERT INTO Devices VALUES(%s,%s, "%s", "%s", "%s", "%s",1)' %(self.userid, generatedId, name,  mac , transport.clientaddr[0], transport.clientaddr[1]) )
        self.cur.execute(query)
	with open(str(generatedId) + '.crt' , 'wb') as outfile:
		outfile.write(crt)
        return myService.AddDeviceResponse.Success

      return myService.AddDeviceResponse.DeviceExists




  def getDevices(self):
    print "getDevices -> " + str(self.userid)
    dev = myService.Device()

    query = ('Select * From Devices Where UserId=%s' %(self.userid) )

    self.cur.execute(query)

    q = self.cur.fetchall()

      
    return [myService.Device(dev[1], dev[2], dev[3], dev[4], dev[5], [], dev[6]) for dev in q]

 

  def logout(self, mac):
    print "logout -> " + mac
    query = ('Update Devices Set Status=0 Where DeviceMac="%s"' %(mac))
    try:
      self.cur.execute(query)
    except Exception as e:
      print e
      return myService.LogoutResponse.Fail
    return myService.LogoutResponse.Success

  def renameDevice(self, mac, name):
    print "renameDevice -> " + mac + "\t" + name
    query = ('Update Devices Set DeviceName="%s" Where DeviceMac="%s"' %(name, mac))
    query2 = ('Select * From Devices Where DeviceMac="%s"' %(mac))

    self.cur.execute(query2)

    try:
      self.cur.fetchone()[0]
    except:
      return myService.RenameDeviceResponse.DeviceNotFound

    try:
      self.cur.execute(query)
    except:
      return myService.RenameDeviceResponse.Fail
    return myService.RenameDeviceResponse.Success

  def updateIp(self, mac):
    newIp = transport.clientaddr[0]
    newPort = transport.clientaddr[1]
    print "updateIP -> " + mac + str(newIp) + str(newPort)

    query = ('Update Devices Set DeviceIp="%s" Where DeviceMac="%s"' %(newIp, mac))
    query2 = ('Update Devices Set DevicePort="%s" Where DeviceMac="%s"' %(newPort, mac))
 
    try:
      self.cur.execute(query)
      self.cur.execute(query2)
    except:
      return myService.UpdateIpResponse.DeviceNotFound
    return myService.UpdateIpResponse.Success

  def getFileMetaData(self, deviceId):
    print "device ID -> " + str(deviceId)

    query = ('Select DeviceIp From Devices Where DeviceId=%s' %(deviceId))

    try:
      self.cur.execute(query)
    except Exception as e:
      print e

    devIp = self.cur.fetchone()[0]
    query = ('Select DevicePort From Devices Where DeviceId=%s' %(deviceId))
    try:
      self.cur.execute(query)
    except Exception as e:
      print e
    devPort = self.cur.fetchone()[0]
    print devIp
    print devPort

    clientSocket= TSSLSocket.TSSLSocket(host=devIp, port=devPort, ca_certs=str(deviceId) + '.crt')
    clientTransport = TTransport.TFramedTransport(clientSocket)
    clientProtocol = TBinaryProtocol.TBinaryProtocol(clientTransport)
    client = clientService.Client(clientProtocol)
    clientTransport.open()

    result = client.getFileMetaData()

    clientTransport.close()

    print result
    return result

  def getFile(self, deviceId, filePath):
    print "device ID -> " + str(deviceId)
    print "file Path -> " + filePath
    query = ('Select DeviceIp From Devices Where DeviceId=%s' %(deviceId))

    try:
      self.cur.execute(query)
    except Exception as e:
      print e

    devIp = self.cur.fetchone()[0]
    query = ('Select DevicePort From Devices Where DeviceId=%s' %(deviceId))
    try:
      self.cur.execute(query)
    except Exception as e:
      print e
    devPort = self.cur.fetchone()[0]
    print devIp
    print devPort

    clientSocket= TSSLSocket.TSSLSocket(host=devIp, port=devPort, ca_certs=str(deviceId) + '.crt')
    clientTransport = TTransport.TFramedTransport(clientSocket)
    clientProtocol = TBinaryProtocol.TBinaryProtocol(clientTransport)
    client = clientService.Client(clientProtocol)
    clientTransport.open()

    result = client.getFileMetaData(filePath)

    clientTransport.close()

    print result
    return result

  

logging.basicConfig()
x = ServerHandler()


processor = myService.Processor(x)
#transport = TSocket.TServerSocket(host='144.122.71.154',port=8081)
try:
  transport = TSSLSocket.TSSLServerSocket(host='144.122.71.154', port=8080, certfile='key/server.pem')
  #tfactory = TTransport.TBufferedTransportFactory()
  pfactory = TBinaryProtocol.TBinaryProtocolFactory()

  tfactory = TTransport.TFramedTransportFactory()
  #pfactory = TTransport.TFramedTransportFactory()
  #server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

  # You could do one of these for a multithreaded server
  #server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
  #server = TNonblockingServer.TNonblockingServer(processor, transport, pfactory, pfactory)
  server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

  print('Starting the server...')
  server.serve()
  print('done.')
except Exception as e:
  print e
