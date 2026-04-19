# validators/auth/register_schema.py


class RegisterSchema:
    def __init__(self, email, password, username):
        self.email = email
        self.password = password
        self.username = username

    def validate(self):
        if not self.email:
            return False, "Email required"

        if not self.password:
            return False, "Password required"

        if len(self.username) < 3:
            return False, "Username too short"

        return True, ""
