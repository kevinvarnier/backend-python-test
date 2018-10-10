from alayatodo import db
import bcrypt

class Users(db.Model): 
    """
    User model
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)

    def check_password(self, password): 
        print(self.password, password)
        if bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8')):
            return True 
            
class Todos(db.Model): 
    """
    Todo model
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Integer, default=0)