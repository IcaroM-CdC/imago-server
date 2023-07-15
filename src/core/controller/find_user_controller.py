import json

from flask            import Request
from misc.status_code import StatusCode
from core.middlewares import EnsureAuthenticated
from core.services    import FindUserService

class FindUserController:
    def handle(self, request:Request):
        ensure_authenticated = EnsureAuthenticated()
        find_user_service    = FindUserService()

        auth = ensure_authenticated.handle(
            request.headers["token"],
            request.headers["username"]
        )

        if (auth):
            response = find_user_service.execute(
                username = request.headers["requested-user"]
            )
        
            if (response):
                return json.dumps({
                    "message": "success" ,"data": response, "status_code": StatusCode.OK
                }), StatusCode.OK
            else:
                return json.dumps({
                    "message": "failed" ,"data": "unexistent", "status_code": StatusCode.Error
                }), StatusCode.Error
        else:
            return json.dumps({
                "message": "unauthorized", "status_code": StatusCode.Unauthorized
            }), StatusCode.Unauthorized