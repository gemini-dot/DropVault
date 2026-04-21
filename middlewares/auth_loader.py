from extensions.LoginManager import login_manager
from models.user import User

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)