from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import Session
from models import animalModel
from schemas import animalSchema


def get_animal(db:Session, animal_id:int):
    return db.query(animalModel.Animal).filter(animalModel.Animal.id == animal_id).first()

def get_animals(db:Session, skip: int = 0, limit : int = 1001):
    return db.query(animalModel.Animal).offset(skip).limit(limit).all()

def create_animal(db: Session, animal : animalSchema.AnimalCreated):


    db_animal = animalModel.Animal(name = animal.name, date_created=animal.date_created,
    
    last_modified=animal.last_modified,danger = animal.danger,wild=animal.wild,notify=animal.notify)

    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)

    return db_animal


def update_animal(db:Session,animal_id:int , payload:animalSchema.AnimalUpdated):

    db_animal = db.query(animalModel.Animal).filter(animalModel.Animal.id == animal_id).first()

    if(db_animal == None):
        return False
    
    if(payload.name != None):    
        setattr(db_animal, 'name', payload.name)

    if(payload.danger != None):    
        setattr(db_animal, 'danger', payload.danger)
    
    if(payload.wild != None ):    
        setattr(db_animal, 'wild', payload.wild)
    
    if(payload.notify != None):    
        setattr(db_animal, 'notify', payload.notify)
    
    setattr(db_animal, 'last_modified', payload.last_modified)


    try:
        db.commit()
        return True
    except InvalidRequestError:
        db.rollback()
        raise InvalidRequestError




def delete_animal(db:Session, animal_id:int):
    db.query(animalModel.Animal).filter(animalModel.Animal.id == animal_id).delete()
    try:
        db.commit()
        return True
    except InvalidRequestError:
        db.rollback()
        raise InvalidRequestError