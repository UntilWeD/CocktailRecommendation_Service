from flask-login import UserMixin

class User(UserMixin):
    def __init__(self, user_id, email, password):
        self.id = user_id
        self.email = email
        self.password = password

    def get_id(self):
        return self.id






