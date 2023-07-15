import sys
sys.dont_write_bytecode = True
import json
import time

from flask            import Flask
from flask            import request

from misc.status_code import StatusCode
from misc.load_config import Configs
from log.logger       import Logger

from core.controller  import CreateUserController
from core.controller  import CreatePostController
from core.controller  import FollowUserController
from core.controller  import AuthUserController
from core.controller  import RetrieveFeedController
from core.controller  import RemoveFollowerController
from core.controller  import RemoveFollowedController
from core.controller  import ListPostsController
from core.controller  import ListFollowersController
from core.controller  import ListFollowedsController
from core.controller  import FindUserController
from core.controller  import UpdateUserController
from core.controller  import ComentPostController
from core.controller  import LikePostController
from core.controller  import UnlikePostController

from core.middlewares import EnsureAuthenticated

status_code                = StatusCode()
configs                    = Configs()
logger                     = Logger()

create_user_controller     = CreateUserController()
create_post_controller     = CreatePostController()
follow_user_controller     = FollowUserController()
auth_user_controller       = AuthUserController()
retrieve_feed_controller   = RetrieveFeedController()
remove_follower_controller = RemoveFollowerController()
remove_followed_controller = RemoveFollowedController()
list_post_controller       = ListPostsController()
list_followers_controller  = ListFollowersController()
list_followeds_controller  = ListFollowedsController()
find_user_controller       = FindUserController()
update_user_controller     = UpdateUserController()
coment_post_controller     = ComentPostController()
like_post_controller       = LikePostController()
unlike_post_controller     = UnlikePostController()

ensure_authenticated       = EnsureAuthenticated()


APP = Flask(__name__)

@APP.errorhandler(404)
def route_not_found(error):
    code, message = str(error).split(": ")
    return json.dumps(
        {
            "message": message, 
            "status_code": 404
        }
    ), 404

# ================================ USER ROUTES ================================

@APP.route("/user/register", methods = ["POST"])
def register():
    begin = time.time()
    
    if (request.method == "POST"):
        response = create_user_controller.handle(request)

        logger.new_rest_log(
            user_ip_address = request.remote_addr, 
            username        = "username", 
            bytes_sent      = sys.getsizeof(response), 
            bytes_received  = sys.getsizeof(request),
            time_spent      = time.time() - begin,
            http_method     = "POST", 
            url             = "/user/register", 
            http_status     = response[1]
        )

        return response

@APP.route("/user/login", methods = ["GET"])
def login():
    begin = time.time()
    
    if (request.method == "GET"):
        response = auth_user_controller.handle(request)
            
        logger.new_rest_log(
            user_ip_address = request.remote_addr, 
            username        = request.headers["username"], 
            bytes_sent      = sys.getsizeof(response), 
            bytes_received  = sys.getsizeof(request),
            time_spent      = time.time() - begin,
            http_method     = "GET", 
            url             = "/user/login", 
            http_status     = response[1]
        )

        return response

# TODO: não deixar a coluna para ser passada como parametro
@APP.route("/user/update", methods = ["PATCH"])
def update_user():
    begin = time.time()

    auth = ensure_authenticated.handle(
        request.headers["token"],
        request.headers["username"]
    )

    if (auth):
        if (request.method == "PATCH"):
            
            content_size = request.headers["Content-Length"]  
            username     = request.headers["username"]
            
            request_parsed = request.get_json() 
            data = request_parsed["data"]
        
            response = update_user_controller.handle(
                username,
                data
            )

            if (response):
                logger.new_rest_log(
                    user_ip_address = request.remote_addr, 
                    username        = username, 
                    bytes_sent      = sys.getsizeof(response), 
                    bytes_received  = content_size,
                    time_spent      = time.time() - begin,
                    http_method     = "PATCH", 
                    url             = "/user/update", 
                    http_status     = status_code.OK
                )
                
                return json.dumps({
                    "message": "success", "status_code": status_code.OK
                }), status_code.OK
            else:
                logger.new_rest_log(
                    user_ip_address = request.remote_addr, 
                    username        = username, 
                    bytes_sent      = 0, 
                    bytes_received  = 0,
                    time_spent      = time.time() - begin,
                    http_method     = "PATCH", 
                    url             = "/user/update", 
                    http_status     = status_code.Error
                )
                
                return json.dumps({
                    "message": "failed", "status_code": status_code.Error
                }), status_code.Error
    else:
        logger.new_rest_log(
            user_ip_address = request.remote_addr, 
            username        = username, 
            bytes_sent      = 0, 
            bytes_received  = 0,
            time_spent      = time.time() - begin,
            http_method     = "PATCH", 
            url             = "/user/update", 
            http_status     = status_code.Unauthorized
        )  
        
        return json.dumps({
            "message": "unauthorized", "status_code": status_code.Unauthorized
        }), status_code.Unauthorized

@APP.route("/user/get", methods = ["GET"])
def get_user():
    begin = time.time()

    if (request.method == "GET"):
        response = find_user_controller.handle(request)

        logger.new_rest_log(
            user_ip_address = request.remote_addr, 
            username        = request.headers["requested-user"], 
            bytes_sent      = sys.getsizeof(response), 
            bytes_received  = sys.getsizeof(request),
            time_spent      = time.time() - begin,
            http_method     = "GET", 
            url             = "/user/get", 
            http_status     = response[1]
        )                

        return response

# ================================ FOLLOW ROUTES ================================

@APP.route("/follow_user", methods = ["POST"])
def follow_user():
    begin = time.time()

    if (request.method == "POST"):
        response = follow_user_controller.handle(request)

        logger.new_rest_log(
            user_ip_address = request.remote_addr, 
            username        = request.headers["username"], 
            bytes_sent      = sys.getsizeof(response), 
            bytes_received  = sys.getsizeof(request),
            time_spent      = time.time() - begin,
            http_method     = "POST", 
            url             = "/follow/user", 
            http_status     = response[1]
        )  
        
        return response

@APP.route("/follow_user/list/followers", methods = ["GET"])
def list_followers():
    begin = time.time()

    if (request.method == "GET"):
        response = list_followers_controller.handle(request)

        logger.new_rest_log(
            user_ip_address = request.remote_addr, 
            username        = request.headers["username"], 
            bytes_sent      = sys.getsizeof(response), 
            bytes_received  = sys.getsizeof(request),
            time_spent      = time.time() - begin,
            http_method     = "GET", 
            url             = "/follow_user/list/followers", 
            http_status     = response[1]
        ) 

        return response
    
@APP.route("/follow_user/list/followeds", methods = ["GET"])
def list_followeds():
    begin = time.time()

    if (request.method == "GET"):
        response = list_followeds_controller.handle(request)

        logger.new_rest_log(
            user_ip_address = request.remote_addr, 
            username        = request.headers["username"], 
            bytes_sent      = sys.getsizeof(response), 
            bytes_received  = sys.getsizeof(request),
            time_spent      = time.time() - begin,
            http_method     = "GET", 
            url             = "/follow_user/list/followeds", 
            http_status     = response[1]
        ) 

        return response

@APP.route("/follow_user/remove/follower", methods = ["DELETE"])
def remove_follower():
    begin = time.time()

    if (request.method == "DELETE"):
        response = remove_follower_controller.handle(request)
        
        logger.new_rest_log(
            user_ip_address = request.remote_addr, 
            username        = request.headers["username"], 
            bytes_sent      = sys.getsizeof(response), 
            bytes_received  = sys.getsizeof(request),
            time_spent      = time.time() - begin,
            http_method     = "DELETE", 
            url             = "/follow_user/remove/follower", 
            http_status     = response[1]
        ) 

        return response
    
@APP.route("/follow_user/remove/followed", methods = ["DELETE"])
def remove_followed():
    begin = time.time()

    if (request.method == "DELETE"):
        response = remove_followed_controller.handle(request)
        
        logger.new_rest_log(
            user_ip_address = request.remote_addr, 
            username        = request.headers["username"], 
            bytes_sent      = sys.getsizeof(response), 
            bytes_received  = sys.getsizeof(request),
            time_spent      = time.time() - begin,
            http_method     = "DELETE", 
            url             = "/follow_user/remove/followed", 
            http_status     = response[1]
        ) 

# ================================ POST ROUTES ================================

@APP.route("/post/new", methods = ["POST"])
def create_post():
    begin = time.time()

    if (request.method == "POST"):
        response = create_post_controller.handle(request)

        logger.new_rest_log(
            user_ip_address = request.remote_addr, 
            username        = request.headers["username"], 
            bytes_sent      = sys.getsizeof(response), 
            bytes_received  = sys.getsizeof(request),
            time_spent      = time.time() - begin,
            http_method     = "POST", 
            url             = "/post/new", 
            http_status     = response[1]
        ) 

        return response

@APP.route("/post/list", methods = ["GET"])
def list_posts():
    begin = time.time()

    if (request.method == "GET"):
        response = list_post_controller.handle(request)

        logger.new_rest_log(
            user_ip_address = request.remote_addr, 
            username        = request.headers["username"], 
            bytes_sent      = sys.getsizeof(response), 
            bytes_received  = sys.getsizeof(request),
            time_spent      = time.time() - begin,
            http_method     = "GET", 
            url             = "/post/list", 
            http_status     = response[1]
        ) 

        return response


@APP.route("/post/like", methods = ["POST"])
def like_post():
    begin = time.time()

    if (request.method == "POST"):
        response = like_post_controller.handle(request)

        logger.new_rest_log(
            user_ip_address = request.remote_addr, 
            username        = request.headers["username"], 
            bytes_sent      = sys.getsizeof(response), 
            bytes_received  = sys.getsizeof(request),
            time_spent      = time.time() - begin,
            http_method     = "POST", 
            url             = "/post/like", 
            http_status     = response[1]
        )

        return response

#TODO: alterar a rota para usar o metodo delete
@APP.route("/post/unlike", methods = ["DELETE"])
def unlike_post():
    begin = time.time()
    
    auth = ensure_authenticated.handle(
        request.headers["token"],
        request.headers["username"]
    )

    if (auth):
        if (request.method == "DELETE"):
            response = unlike_post_controller.handle(request)

            logger.new_rest_log(
                user_ip_address = request.remote_addr, 
                username        = request.headers["username"], 
                bytes_sent      = sys.getsizeof(response), 
                bytes_received  = sys.getsizeof(request),
                time_spent      = time.time() - begin,
                http_method     = "POST", 
                url             = "/post/unlike", 
                http_status     = status_code.OK
            )

        return response

@APP.route("/post/coment", methods = ["POST"])
def coment_post():
    begin = time.time()

    if (request.method == "POST"):
        response = coment_post_controller.handle(request)

        logger.new_rest_log(
            user_ip_address = request.remote_addr, 
            username        = request.headers["username"], 
            bytes_sent      = sys.getsizeof(response), 
            bytes_received  = sys.getsizeof(request),
            time_spent      = time.time() - begin,
            http_method     = "POST", 
            url             = "/post/coment", 
            http_status     = response[1]
        )

        return response


# ================================ FEED ROUTES ================================

@APP.route("/feed/retrieve", methods = ["GET"])
def retrieve_feed():
    begin = time.time()

    if (request.method == "GET"):
        response = retrieve_feed_controller.handle(request)
        
        logger.new_rest_log(
            user_ip_address = request.remote_addr, 
            username        = request.headers["username"], 
            bytes_sent      = sys.getsizeof(response), 
            bytes_received  = sys.getsizeof(request),
            time_spent      = time.time() - begin,
            http_method     = "GET", 
            url             = "/feed/retrieve", 
            http_status     = response[1]
        )

        return response


if (__name__ == "__main__"):
    
    port  = configs.config["server"]["rest_port"]
    debug = configs.config["server"]["debug"] 
    ip    = configs.config["server"]["ip_address"]
    
    print(f"> Starting server at http://{ip}:{port}")
    
    APP.run(debug=debug, port=port)
    