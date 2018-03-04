namespace py project

enum AddGroupResponse{
  Success=0
  Fail = 1
  AuthenticationFail = 99
}

enum AddUserToGroupResponse{
  Success=0
  Fail = 1
  AuthenticationFail = 99
} 

enum AddDeviceToGroupResponse{
  Success=0
  Fail = 1
  AuthenticationFail = 99
}

enum AddDeviceToFacebookResponse{
  Success=0
  Fail = 1
  AuthenticationFail = 99
}

enum LogoutResponse{
  Success = 0
  Fail = 1
  AuthenticationFail = 99
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
  AuthenticationFail = 99
}

enum RenameDeviceResponse{
  Success = 0
  DeviceNotFound = 1
  Fail = 2
  AuthenticationFail = 9
}

enum UpdateIpResponse{
  Success = 0
  DeviceNotFound = 1
  Fail = 2
  AuthenticationFail = 99
}

struct Device{
  1: required i64 id,
  2: optional string name,
  3: optional string mac,
  4: optional string ip,
  5: optional string port,
  6: optional string functionality,
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

  string login(1:string username, 2:string password, 3:string mac),

  LogoutResponse logout(1:string mac, 2:string key),

  AddDeviceResponse addDevice(1:string mac, 2:string devicename, 3:binary certfile, 4:string capabilities, 5:string rsakey, 6:string key),

  RenameDeviceResponse renameDevice(1:string mac, 2:string devicename, 3:string key),

  UpdateIpResponse updateIp(1:string mac, 2:string key),

  list<Device> getDevices(1:string key),

  string getGroups(1:list<string> friends, 2:string key),
  
  AddGroupResponse addGroup(1:string gname, 2:string key),

  AddUserToGroupResponse addUserToGroup(1:i64 gid, 2:string username, 3:string key),

  AddDeviceToGroupResponse addDeviceToGroup(1:i64 gid, 2:string device, 3:string key),

  AddDeviceToFacebookResponse addDeviceToFacebook(1:string device, 2:string key)

}
