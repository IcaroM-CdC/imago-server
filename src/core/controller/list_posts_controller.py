import json

from flask            import Request
from misc.status_code import StatusCode
from core.middlewares import EnsureAuthenticated
from core.services    import ListPostsService

class ListPostsController:
    def handle(self, request:Request): # retorna um array de posts
        ensure_authenticated = EnsureAuthenticated()
        list_posts_service   = ListPostsService()

        auth = ensure_authenticated.handle(
            request.headers["token"],
            request.headers["username"]
        )

        if (auth):

            response = list_posts_service.execute(
                username        = request.headers["username"], 
                target_username = request.headers["target-username"]
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