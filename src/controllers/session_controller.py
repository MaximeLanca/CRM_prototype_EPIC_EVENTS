from src.services.session_service import SessionService

class SessionController:
    def __init__(self):
        self.service = SessionService()
    
    def get_payload(self):
        return self.service.get_payload()
    
    def generate_token(self, user):
        return self.service.generate_token(user)


