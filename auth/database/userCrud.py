from sqlalchemy.orm import Session
from sqlalchemy.exc import InvalidRequestError

from  models import userModel 
from  schemas import userSchema
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db:Session, user_id:int):
    return db.query(userModel.User).filter(userModel.User.id == user_id).first()

def get_user_by_email(db:Session, username:str):
    return db.query(userModel.User).filter(userModel.User.username == username).first()

def get_users(db:Session, skip: int = 0, limit: int =100):
    return db.query(userModel.User).offset(skip).limit(limit).all()

def create_user(db: Session, user:userSchema.UserCreate):
    
    hashed_password = pwd_context.hash(user.password)
    db_user = userModel.User(username = user.username, hashed_password=hashed_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db:Session, user_id:int):
    db.query(userModel.User).filter(userModel.User.id == user_id).delete()
    try:
        db.commit()
        return True
    except InvalidRequestError:
        db.rollback()
        raise InvalidRequestError



def update_user(db:Session, user_id:int , payload:userSchema.UserUpdate):

    db_user = db.query(userModel.User).filter(userModel.User.id == user_id).first()
    
    if(db_user):
        hashed_password = pwd_context.hash(payload.password)
        setattr(db_user, 'hashed_password',hashed_password )
    else:
        return False  

    try:
        db.commit()
        return True
    except InvalidRequestError:
        db.rollback()
        raise InvalidRequestError