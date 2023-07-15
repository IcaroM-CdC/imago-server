import json

from flask            import Request
from misc.status_code import StatusCode
from core.middlewares import EnsureAuthenticated
from core.services    import ListPostsService

class ListPostsController:
    def __init__(self):
        self.response_ids = (
            "id", 
            "description",
            "likes",
            "created_date",
            "created_time",
            "image",
            "owner",
            "owner_id",
            "already_liked"
        )
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
                formated_response = []

                for post in response:
                    formated_response.append(dict(zip(self.response_ids, post)))

                return json.dumps({
                    "message": "success", "data": formated_response, "status_code": StatusCode.OK
                }), StatusCode.OK
            else:
                return json.dumps({
                        "message": "failed", "data": "", "status_code": StatusCode.Error
                    }), StatusCode.Error
        else:
            return json.dumps({
                "message": "unauthorized", "status_code": StatusCode.Unauthorized
            }), StatusCode.Unauthorized