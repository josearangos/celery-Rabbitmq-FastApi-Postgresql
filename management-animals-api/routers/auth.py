from fastapi import APIRouter, Body,Depends,HTTPException,status
from fastapi.security import  OAuth2PasswordRequestForm, OAuth2PasswordBearer
import json
import requests
from decouple import config


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


router = APIRouter()



@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    
    params = {"username":form_data.username, "password":form_data.password}

    url = config("USER_API_HOST")+config("ENPOINT_LOGIN")
    
    response =  requests.post(url,data=params) 

    response = json.loads(response.content)

       
    if 'detail' in response:

        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
        )

    return response


@router.get("/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):

    url = config("USER_API_HOST")+config("ENPOINT_ME")

    hed = {'Authorization': 'Bearer ' + token}

    response =  requests.get(url,headers=hed) 

    return json.loads(response.content)