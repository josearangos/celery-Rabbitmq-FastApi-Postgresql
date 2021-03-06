from models import animalModel
from schemas import animalSchema
from database.connection import SessionLocal, engine
from database import animalCrud
from sqlalchemy.orm import Session
from typing import List
import datetime
import requests
from decouple import config
from fastapi.security import  OAuth2PasswordRequestForm, OAuth2PasswordBearer
import json

from fastapi import APIRouter, Body,Depends,HTTPException
animalModel.Base.metadata.create_all(bind=engine)

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

@router.get("/",response_model=List[animalSchema.Animal])
def read_animals(skip: int = 0 , limit: int = 100, db:Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    animals = animalCrud.get_animals(db,skip=skip,limit=limit)
    return animals


@router.post("/")
def create_animal(animal: animalSchema.AnimalBase, db:Session = Depends(get_db),token: str = Depends(oauth2_scheme)):

    last_modified = datetime.datetime.now()
    date_created = datetime.datetime.now()

    n_animal = animalSchema.AnimalCreated(notify = animal.notify,wild = animal.wild,name=animal.name,danger = animal.danger,last_modified=last_modified,date_created=date_created)

    #Send email
    url = config("URL_CELERY_API")+config("END_POINT_SEND_EMAIL")
    # Get email

    url_me = config("USER_API_HOST")+config("ENPOINT_ME")

    hed = {'Authorization': 'Bearer ' + token}

    response = requests.get(url_me,headers =hed)

    email = json.loads(response.content)["username"]
    
    # Send email

    inp_post_response = requests.post(url,json={"email":email})

    
    animal =  animalCrud.create_animal(db=db, animal=n_animal)

    return {"code":200,"message":"Animal added successfully"}


@router.delete("/")
def delete_animal(animal_id: int,db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    response =  animalCrud.delete_animal(db=db,animal_id=animal_id)

    if(response == False):
        return {"code":400,"message":"Animal deleted error"}

    return {"code":200,"message":"Animal deleted successfully"}


@router.put("/")
def update_animal(animal:animalSchema.AnimalUpdate,db:Session = Depends(get_db),token: str = Depends(oauth2_scheme)):

    last_modified = datetime.datetime.now()

    n_animal = animalSchema.AnimalUpdated(id = animal.id,notify = animal.notify,wild = animal.wild,name=animal.name,danger = animal.danger,last_modified=last_modified)

    response =  animalCrud.update_animal(db=db,animal_id=animal.id,payload=n_animal)

    if (response == False):

        return {"code":400,"message":"Animal updated error"}
    
    return {"code":200,"message":"Animal updated successfully"}
