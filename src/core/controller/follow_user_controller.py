import json

from flask            import Request
from misc.status_code import StatusCode
from core.middlewares import EnsureAuthenticated
from core.services    import FollowUserService

class FollowUserController:
    def handle(self, request:Request):
        ensure_authenticated = EnsureAuthenticated()
        follow_user_service  = FollowUserService()

        auth = ensure_authenticated.handle(
            request.headers["token"],
            request.headers["username"]
        )

        if (auth):
            request_parsed = request.get_json() 

            response = follow_user_service.execute(
                followed_username = request_parsed["followed_user"], 
                follower_username = request_parsed["follower_user"]
            )

            if (response):
                return json.dumps({
                    "message": "success", "status_code": StatusCode.OK 
                }), StatusCode.OK      
            else:
                return json.dumps({
                    "message": "failed", "status_code": StatusCode.Error 
                }), StatusCode.Error  
        else:
            return json.dumps({
                "message": "unauthorized", "status_code": StatusCode.Unauthorized
            }), StatusCode.Unauthorized