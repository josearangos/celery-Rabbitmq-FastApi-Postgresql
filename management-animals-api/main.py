from fastapi import FastAPI

#Routes
from routers.animal import router as animalRouter


app = FastAPI(title="Animal Management System")


#Include routes
app.include_router(animalRouter,tags=["Animal"],prefix='/animal')


@app.get("/")
def read_root():
    return {"Hello": "World"}