from backend.db_handler.base_handler import BaseDBHandler
from backend.models.user_login import UserLogin


class UserLoginDBHandler(BaseDBHandler):
    def __init__(self):
        super().__init__(model=UserLogin)


user_login_db_handler = UserLoginDBHandler()
