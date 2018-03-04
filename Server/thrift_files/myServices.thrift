namespace py project


enum LogoutResponse{
  Success = 0
  Fail = 1
}

enum LoginResponse{
  Success = 0
  SuccessNewDevice = 1
  WrongInfo = 2
  Fail = 3

}

enum RegisterResponse{
  Success = 0
  UsernameExists = 1
  EmailExists = 2
  Fail = 3
}

enum AddDeviceResponse{
  Success = 0
  DeviceExists = 1
  Fail = 2

}

enum RenameDeviceResponse{
  Success = 0
  DeviceNotFound = 1
  Fail = 2
}

enum UpdateIpResponse{
  Success = 0
  DeviceNotFound = 1
  Fail = 2
}

struct Device{
  1: required i64 id,
  2: optional string name,
  3: optional string mac,
  4: optional string ip,
  5: optional string port,
  6: optional list<bool> functionality,
  7: optional i64 status,
  8: optional binary certfile
}


struct UserProfile{
  1: required i64 id,
  2: optional string username,
  3: optional string password,    
  4: optional string name,
  5: optional string email,
  6: optional list<Device> devices
}



/**
 * The Thrift Service API of the Application 
 */
service myService {

  RegisterResponse registerRequest(1:string username, 2:string password, 3:string name, 4:string email),

  LoginResponse login(1:string username, 2:string password, 3:string mac),

  LogoutResponse logout(1:string mac),

  AddDeviceResponse addDevice(1:string mac, 2:string devicename, 3:binary certfile),

  RenameDeviceResponse renameDevice(1:string mac, 2:string devicename),

  UpdateIpResponse updateIp(1:string mac),

  list<Device> getDevices()

}