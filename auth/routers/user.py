from models import userModel
from schemas import userSchema
from database.connection import SessionLocal, engine
from database import userCrud
from sqlalchemy.orm import Session

from typing import List


from fastapi import APIRouter, Body,Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer

userModel.Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


router = APIRouter()


def get_db():
    db = SessionLocal()
    """
    De esta manera nos aseguramos de que la sesión de la base de datos siempre se cierre después de la solicitud. 
    Incluso si hubo una excepción al procesar la solicitud.
    """
    try:
        yield db
    finally:
        db.close()


@router.get("/",response_model=List[userSchema.User])
def read_users(skip: int = 0 , limit: int = 100, db:Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    users = userCrud.get_users(db,skip=skip,limit=limit)
    return users




@router.post("/",response_model=userSchema.User)
def create_user(user: userSchema.UserCreate, db:Session = Depends(get_db)):
    
    db_user = userCrud.get_user_by_email(db,user.username)

    if(db_user):
        raise HTTPException(status_code= 400, detail="Email already registered")

    return userCrud.create_user(db=db, user=user)


@router.delete("/")
def delete_user(user_id: int,db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    return userCrud.delete_user(db=db,user_id=user_id)

@router.put("/")
def update_user(user:userSchema.UserUpdate,db:Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    return userCrud.update_user(db=db,user_id=user.id,payload=user)
