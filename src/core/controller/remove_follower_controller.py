import json

from flask            import Request
from misc.status_code import StatusCode
from core.middlewares import EnsureAuthenticated
from core.services    import RemoveFollowerService

class RemoveFollowerController:
    def handle(self, request:Request):
        ensure_authenticated    = EnsureAuthenticated()
        remove_follower_service = RemoveFollowerService()
        
        auth = ensure_authenticated.handle(
            request.headers["token"],
            request.headers["username"]
        )

        if (auth):
            request_parsed = request.get_json()
            
            response = remove_follower_service.execute(
                followed_username = request_parsed["followed"],
                follower_username = request.headers["username"]
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
            