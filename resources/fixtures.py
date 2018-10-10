from alayatodo import db
from alayatodo.models import Users
import bcrypt

def create_users():

    credentials = ['user1', 'user2', 'user3']

    for credential in credentials : 
        passwordhashed = bcrypt.hashpw(credential, bcrypt.gensalt())
        user = Users(username = credential, password = passwordhashed)
        db.session.add(user)

    db.session.commit()
  