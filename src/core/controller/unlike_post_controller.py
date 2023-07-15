import json

from flask            import Request
from misc.status_code import StatusCode
from core.middlewares import EnsureAuthenticated
from core.services    import UnlikePostsService

class UnlikePostController:
    def handle(self, request:Request):
        ensure_authenticated = EnsureAuthenticated()
        unlike_post_service  = UnlikePostsService()

        auth = ensure_authenticated.handle(
            request.headers["token"],
            request.headers["username"]
        )

        if (auth):
            request_parsed = request.get_json()

            response = unlike_post_service.execute(
                username = request.headers["username"], 
                post_id  = request_parsed["post_id"]
            )

            if (response):
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
        
        return response