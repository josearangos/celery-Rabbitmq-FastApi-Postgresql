from sqlalchemy.orm import Session
from typing import Optional
from fastapi import Depends,HTTPException,status,APIRouter


from database.connection import SessionLocal
from database import userCrud
from schemas import userSchema
from schemas.tokenSchema import TokenData
from typing import List
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from decouple import config


router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config("ACCESS_TOKEN_EXPIRE_MINUTES"))


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependency
"""
Crea una sesion por solicitud luego de que se resuelve se cierra
Nuestra dependencia creará un nuevo SQLAlchemy SessionLocal que se usará en una sola solicitud
 y luego lo cerrará una vez que finalice la solicitud.
"""
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


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db, username: str, password: str):

    user = userCrud.get_user_by_email(db,username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token( data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme),db:Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    
    user = userCrud.get_user_by_email(db,username)



    if user is None:
        raise credentials_exception
    return user



@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    
    user = authenticate_user(db,form_data.username, form_data.password)


    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    # Ojo siempre se debe retornar el access_token y token_type


    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=userSchema.User)
async def read_users_me(current_user: userSchema.User = Depends(get_current_user)):
    return current_user