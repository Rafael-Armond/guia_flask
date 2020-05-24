from guia_flask import db, login_manager, app
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

# Model de usuário
class User(db.Model,UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    urole = db.Column(db.String, server_default="user")

    def __init__(self, _name, _password, _email, _urole='user'):
        self.name = _name
        self.password = _password
        self.email = _email
        self.urole = _urole

    def get_urole(self):
        return self.urole
    
    def check_password(self,_password):
        bcrypt = Bcrypt()
        return bcrypt.check_password_hash(self.password,_password)
    
    def __repr__(self):
        return f"<Id: {self.id}, Name: {self.name}, E-mail: {self.email}.>"
        