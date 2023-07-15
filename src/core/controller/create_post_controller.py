import json

from flask            import Request
from misc.status_code import StatusCode
from core.middlewares import EnsureAuthenticated
from core.services    import CreatePostService

class CreatePostController:
    def handle(self, request:Request):
        ensure_authenticated = EnsureAuthenticated()
        create_post_service  = CreatePostService()

        auth = ensure_authenticated.handle(
            request.headers["token"],
            request.headers["username"]
        )

        if (auth):
            request_parsed = request.get_json()

            response = create_post_service.execute(
                username    = request_parsed["username"], 
                description = request_parsed["description"], 
                image       = request_parsed["image"]
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