import json

from flask            import Request
from misc.status_code import StatusCode
from core.middlewares import EnsureAuthenticated
from core.services import RetrieveFeedService

class RetrieveFeedController:
    def handle(self, request:Request): # retorna um array de posts
        ensure_authenticated = EnsureAuthenticated()
        retrieve_feed_service = RetrieveFeedService()

        auth = ensure_authenticated.handle(
            request.headers["token"],
            request.headers["username"]
        )

        if (auth):
            response = retrieve_feed_service.execute(
                username    = request.headers["username"], 
                posts_limit = request.headers["post-limit"]
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