import json

from flask            import Request
from misc.status_code import StatusCode
from core.services    import CreateUserService

class CreateUserController:
    def handle(self, request:Request):
        create_user_service = CreateUserService()
        
        request_parsed = request.get_json() 
        
        response = create_user_service.execute(
            username    = request_parsed["username"], 
            password    = request_parsed["password"], 
            description = request_parsed["description"]
        )

        if (response == StatusCode.OK):
            return json.dumps({ 
                "message": "success", "status_code": StatusCode.OK 
            }), StatusCode.OK    
        
        elif (response == StatusCode.UserExists): 
            return json.dumps({ 
                "message": "user already exist", "status_code": StatusCode.UserExists 
            }), StatusCode.Error
            
        elif (response == StatusCode.InvalidUsername):
            return json.dumps({ 
                "message": "invalid username", "status_code": StatusCode.InvalidUsername 
            }), StatusCode.Error 