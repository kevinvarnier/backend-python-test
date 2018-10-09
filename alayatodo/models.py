from alayatodo import db

class Users(db.Model): 
    """
    User model
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)

class Todos(db.Model): 
    """
    Todo model
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Integer, default=0)