from fastapi import APIRouter, Body,Depends,HTTPException
from fastapi import params
from schemas import userSchema
from typing import List
import requests
import json
from fastapi.security import OAuth2PasswordBearer
from decouple import config


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

router = APIRouter()


@router.get("/")
def read_users(skip: int = 0 , limit: int = 100,token: str = Depends(oauth2_scheme)):
    

    hed = {'Authorization': 'Bearer ' + token}

    response = requests.get(config("USER_API_HOST")+config("ENPOINT_USER"),data={"skip":skip,"limit":limit},headers=hed)



    return json.loads(response.content)

@router.post("/")
def create_user(user: userSchema.UserCreate):
    
    response = requests.post(config("USER_API_HOST")+config("ENPOINT_USER"),json=user.dict())
    return json.loads(response.content)

@router.delete("/")
def delete_user(user_id: int,token: str = Depends(oauth2_scheme)):

    hed = {'Authorization': 'Bearer ' + token}
    response = requests.delete(config("USER_API_HOST")+config("ENPOINT_USER"),params={"user_id":user_id},headers=hed)
    
    return json.loads(response.content)

@router.put("/")
def update_user(user:userSchema.UserUpdate,token: str = Depends(oauth2_scheme)):
    hed = {'Authorization': 'Bearer ' + token}
    response = requests.put(config("USER_API_HOST")+config("ENPOINT_USER"),json=user.dict(),headers=hed)
    return json.loads(response.content)



