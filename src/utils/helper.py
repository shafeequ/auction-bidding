from app_constants import AppConstants, ResponseMessages

def Singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


def allowedRole(roles = None):
    def decorator(func):
        def decorated(self, *args, **kwargs):
            user = self.request.headers.get('Authorization', None)
 
            # User is refused INVALID_USER
            if user is None:
                self.send_error_response(ResponseMessages.AUTH_HEADER_NOT_FOUND)

            # User is refused 
            if user not in AppConstants.USERS_LIST.keys():
                self.send_error_response(ResponseMessages.INVALID_USER) 

            if AppConstants.ROLES.get(roles) != AppConstants.USERS_LIST.get(user)["role"] :
                self.send_error_response(ResponseMessages.USER_OPR_NOT_PERMITTED) 
                
            self.role = AppConstants.USERS_LIST.get(user)["role"]
            self.user_id = AppConstants.USERS_LIST.get(user)["id"]

            return func(self, *args, **kwargs)
        return decorated
    return decorator