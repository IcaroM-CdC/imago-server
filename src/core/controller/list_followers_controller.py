import json

from flask            import Request
from misc.status_code import StatusCode
from core.middlewares import EnsureAuthenticated
from core.services    import ListFollowersService

class ListFollowersController:
    def __init__(self):
        self.response_ids = (
            "id", 
            "username", 
        )
    def handle(self, request:Request): # retorna um array de posts
        ensure_authenticated   = EnsureAuthenticated()
        list_followers_service = ListFollowersService()

        auth = ensure_authenticated.handle(
            request.headers["token"],
            request.headers["username"]
        )

        if (auth):
            response = list_followers_service.execute(
                username = request.headers["target-user"]
            )
        
            if (isinstance(response, list)):
                formated_response = []

                for user in response:
                    formated_response.append(dict(zip(self.response_ids, user)))

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
