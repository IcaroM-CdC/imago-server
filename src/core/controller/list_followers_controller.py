import json

from flask            import Request
from misc.status_code import StatusCode
from core.middlewares import EnsureAuthenticated
from core.services    import ListFollowersService

class ListFollowersController:
    def handle(self, request:Request): # retorna um array de posts
        ensure_authenticated   = EnsureAuthenticated()
        list_followers_service = ListFollowersService()

        auth = ensure_authenticated.handle(
            request.headers["token"],
            request.headers["username"]
        )

        if (auth):
            response = list_followers_service.execute(
                followed_username = request.headers["username"]
            )
        
            if (isinstance(response, list)):
                return json.dumps({
                    "message": "success", "data": response, "status_code": StatusCode.OK
                }), StatusCode.OK
            else:
                return json.dumps({
                    "message": "failed", "data": "", "status_code": StatusCode.Error
                }), StatusCode.Error

        else:
            return json.dumps({
                "message": "unauthorized", "status_code": StatusCode.Unauthorized
            }), StatusCode.Unauthorized
