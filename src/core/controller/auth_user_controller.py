import json

from flask            import Request
from misc.status_code import StatusCode
from core.services    import AuthUserService

class AuthUserController:
    def handle(self, request:Request):
        authUserService = AuthUserService()

        username     = request.headers["username"]
        password     = request.headers["password"]

        response = authUserService.execute(username, password)
        
        if (response):
            return json.dumps({
                "message": "authenticated", 
                "token": response,
                "status_code": StatusCode.OK
            }), StatusCode.OK
        else:
            return json.dumps({
                "message": "authentication failed", 
                "token": "",
                "status_code": StatusCode.Unauthorized
            }), StatusCode.Unauthorized