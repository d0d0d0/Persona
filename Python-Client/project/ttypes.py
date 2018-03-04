#
# Autogenerated by Thrift Compiler (0.9.1)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException

from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None


class AddGroupResponse:
  Success = 0
  Fail = 1
  AuthenticationFail = 99

  _VALUES_TO_NAMES = {
    0: "Success",
    1: "Fail",
    99: "AuthenticationFail",
  }

  _NAMES_TO_VALUES = {
    "Success": 0,
    "Fail": 1,
    "AuthenticationFail": 99,
  }

class AddUserToGroupResponse:
  Success = 0
  Fail = 1
  AuthenticationFail = 99

  _VALUES_TO_NAMES = {
    0: "Success",
    1: "Fail",
    99: "AuthenticationFail",
  }

  _NAMES_TO_VALUES = {
    "Success": 0,
    "Fail": 1,
    "AuthenticationFail": 99,
  }

class AddDeviceToGroupResponse:
  Success = 0
  Fail = 1
  AuthenticationFail = 99

  _VALUES_TO_NAMES = {
    0: "Success",
    1: "Fail",
    99: "AuthenticationFail",
  }

  _NAMES_TO_VALUES = {
    "Success": 0,
    "Fail": 1,
    "AuthenticationFail": 99,
  }

class AddDeviceToFacebookResponse:
  Success = 0
  Fail = 1
  AuthenticationFail = 99

  _VALUES_TO_NAMES = {
    0: "Success",
    1: "Fail",
    99: "AuthenticationFail",
  }

  _NAMES_TO_VALUES = {
    "Success": 0,
    "Fail": 1,
    "AuthenticationFail": 99,
  }

class LogoutResponse:
  Success = 0
  Fail = 1
  AuthenticationFail = 99

  _VALUES_TO_NAMES = {
    0: "Success",
    1: "Fail",
    99: "AuthenticationFail",
  }

  _NAMES_TO_VALUES = {
    "Success": 0,
    "Fail": 1,
    "AuthenticationFail": 99,
  }

class LoginResponse:
  Success = 0
  SuccessNewDevice = 1
  WrongInfo = 2
  Fail = 3

  _VALUES_TO_NAMES = {
    0: "Success",
    1: "SuccessNewDevice",
    2: "WrongInfo",
    3: "Fail",
  }

  _NAMES_TO_VALUES = {
    "Success": 0,
    "SuccessNewDevice": 1,
    "WrongInfo": 2,
    "Fail": 3,
  }

class RegisterResponse:
  Success = 0
  UsernameExists = 1
  EmailExists = 2
  Fail = 3

  _VALUES_TO_NAMES = {
    0: "Success",
    1: "UsernameExists",
    2: "EmailExists",
    3: "Fail",
  }

  _NAMES_TO_VALUES = {
    "Success": 0,
    "UsernameExists": 1,
    "EmailExists": 2,
    "Fail": 3,
  }

class AddDeviceResponse:
  Success = 0
  DeviceExists = 1
  Fail = 2
  AuthenticationFail = 99

  _VALUES_TO_NAMES = {
    0: "Success",
    1: "DeviceExists",
    2: "Fail",
    99: "AuthenticationFail",
  }

  _NAMES_TO_VALUES = {
    "Success": 0,
    "DeviceExists": 1,
    "Fail": 2,
    "AuthenticationFail": 99,
  }

class RenameDeviceResponse:
  Success = 0
  DeviceNotFound = 1
  Fail = 2
  AuthenticationFail = 9

  _VALUES_TO_NAMES = {
    0: "Success",
    1: "DeviceNotFound",
    2: "Fail",
    9: "AuthenticationFail",
  }

  _NAMES_TO_VALUES = {
    "Success": 0,
    "DeviceNotFound": 1,
    "Fail": 2,
    "AuthenticationFail": 9,
  }

class UpdateIpResponse:
  Success = 0
  DeviceNotFound = 1
  Fail = 2
  AuthenticationFail = 99

  _VALUES_TO_NAMES = {
    0: "Success",
    1: "DeviceNotFound",
    2: "Fail",
    99: "AuthenticationFail",
  }

  _NAMES_TO_VALUES = {
    "Success": 0,
    "DeviceNotFound": 1,
    "Fail": 2,
    "AuthenticationFail": 99,
  }


class Device:
  """
  Attributes:
   - id
   - name
   - mac
   - ip
   - port
   - functionality
   - status
   - certfile
  """

  thrift_spec = (
    None, # 0
    (1, TType.I64, 'id', None, None, ), # 1
    (2, TType.STRING, 'name', None, None, ), # 2
    (3, TType.STRING, 'mac', None, None, ), # 3
    (4, TType.STRING, 'ip', None, None, ), # 4
    (5, TType.STRING, 'port', None, None, ), # 5
    (6, TType.STRING, 'functionality', None, None, ), # 6
    (7, TType.I64, 'status', None, None, ), # 7
    (8, TType.STRING, 'certfile', None, None, ), # 8
  )

  def __init__(self, id=None, name=None, mac=None, ip=None, port=None, functionality=None, status=None, certfile=None,):
    self.id = id
    self.name = name
    self.mac = mac
    self.ip = ip
    self.port = port
    self.functionality = functionality
    self.status = status
    self.certfile = certfile

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I64:
          self.id = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.name = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.STRING:
          self.mac = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.STRING:
          self.ip = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.STRING:
          self.port = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 6:
        if ftype == TType.STRING:
          self.functionality = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 7:
        if ftype == TType.I64:
          self.status = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 8:
        if ftype == TType.STRING:
          self.certfile = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('Device')
    if self.id is not None:
      oprot.writeFieldBegin('id', TType.I64, 1)
      oprot.writeI64(self.id)
      oprot.writeFieldEnd()
    if self.name is not None:
      oprot.writeFieldBegin('name', TType.STRING, 2)
      oprot.writeString(self.name)
      oprot.writeFieldEnd()
    if self.mac is not None:
      oprot.writeFieldBegin('mac', TType.STRING, 3)
      oprot.writeString(self.mac)
      oprot.writeFieldEnd()
    if self.ip is not None:
      oprot.writeFieldBegin('ip', TType.STRING, 4)
      oprot.writeString(self.ip)
      oprot.writeFieldEnd()
    if self.port is not None:
      oprot.writeFieldBegin('port', TType.STRING, 5)
      oprot.writeString(self.port)
      oprot.writeFieldEnd()
    if self.functionality is not None:
      oprot.writeFieldBegin('functionality', TType.STRING, 6)
      oprot.writeString(self.functionality)
      oprot.writeFieldEnd()
    if self.status is not None:
      oprot.writeFieldBegin('status', TType.I64, 7)
      oprot.writeI64(self.status)
      oprot.writeFieldEnd()
    if self.certfile is not None:
      oprot.writeFieldBegin('certfile', TType.STRING, 8)
      oprot.writeString(self.certfile)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    if self.id is None:
      raise TProtocol.TProtocolException(message='Required field id is unset!')
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class UserProfile:
  """
  Attributes:
   - id
   - username
   - password
   - name
   - email
   - devices
  """

  thrift_spec = (
    None, # 0
    (1, TType.I64, 'id', None, None, ), # 1
    (2, TType.STRING, 'username', None, None, ), # 2
    (3, TType.STRING, 'password', None, None, ), # 3
    (4, TType.STRING, 'name', None, None, ), # 4
    (5, TType.STRING, 'email', None, None, ), # 5
    (6, TType.LIST, 'devices', (TType.STRUCT,(Device, Device.thrift_spec)), None, ), # 6
  )

  def __init__(self, id=None, username=None, password=None, name=None, email=None, devices=None,):
    self.id = id
    self.username = username
    self.password = password
    self.name = name
    self.email = email
    self.devices = devices

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I64:
          self.id = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.username = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.STRING:
          self.password = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.STRING:
          self.name = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.STRING:
          self.email = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 6:
        if ftype == TType.LIST:
          self.devices = []
          (_etype3, _size0) = iprot.readListBegin()
          for _i4 in xrange(_size0):
            _elem5 = Device()
            _elem5.read(iprot)
            self.devices.append(_elem5)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('UserProfile')
    if self.id is not None:
      oprot.writeFieldBegin('id', TType.I64, 1)
      oprot.writeI64(self.id)
      oprot.writeFieldEnd()
    if self.username is not None:
      oprot.writeFieldBegin('username', TType.STRING, 2)
      oprot.writeString(self.username)
      oprot.writeFieldEnd()
    if self.password is not None:
      oprot.writeFieldBegin('password', TType.STRING, 3)
      oprot.writeString(self.password)
      oprot.writeFieldEnd()
    if self.name is not None:
      oprot.writeFieldBegin('name', TType.STRING, 4)
      oprot.writeString(self.name)
      oprot.writeFieldEnd()
    if self.email is not None:
      oprot.writeFieldBegin('email', TType.STRING, 5)
      oprot.writeString(self.email)
      oprot.writeFieldEnd()
    if self.devices is not None:
      oprot.writeFieldBegin('devices', TType.LIST, 6)
      oprot.writeListBegin(TType.STRUCT, len(self.devices))
      for iter6 in self.devices:
        iter6.write(oprot)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    if self.id is None:
      raise TProtocol.TProtocolException(message='Required field id is unset!')
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)