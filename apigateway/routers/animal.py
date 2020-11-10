from fastapi import APIRouter, Body,Depends,HTTPException,status
from fastapi.security import  OAuth2PasswordRequestForm, OAuth2PasswordBearer
import json
import requests
from decouple import config
from schemas import animalSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


router = APIRouter()


@router.get("/")
def read_users(skip: int = 0 , limit: int = 100,token: str = Depends(oauth2_scheme)):
    
    hed = {'Authorization': 'Bearer ' + token}
    response = requests.get(config("ANIMA_API_HOST")+config("ENPOINT_ANIMAL"),data={"skip":skip,"limit":limit},headers=hed)
    return json.loads(response.content)


@router.post("/")
def create_user(animal: animalSchema.AnimalBase,token: str = Depends(oauth2_scheme)): 
    hed = {'Authorization': 'Bearer ' + token}   
    response = requests.post(config("ANIMA_API_HOST")+config("ENPOINT_ANIMAL"),json=animal.dict(),headers=hed)
    return json.loads(response.content)

@router.delete("/")
def delete_animal(animal_id: int,token: str = Depends(oauth2_scheme)):
    hed = {'Authorization': 'Bearer ' + token}
    response = requests.delete(config("ANIMA_API_HOST")+config("ENPOINT_ANIMAL"),params={"animal_id":animal_id},headers=hed)
    return json.loads(response.content)

@router.put("/")
def update_animal(animal:animalSchema.AnimalUpdate,token: str = Depends(oauth2_scheme)):
    hed = {'Authorization': 'Bearer ' + token}
    response = requests.put(config("ANIMA_API_HOST")+config("ENPOINT_ANIMAL"),json=animal.dict(),headers=hed)
    return json.loads(response.content)
