from fastapi import FastAPI

#Routes
from routers.animal import router as animalRouter
from routers.auth import router as authRouter

app = FastAPI(title="Animal Management System")


#Include routes
app.include_router(animalRouter,tags=["Animal"],prefix='/animal')
app.include_router(authRouter,tags=["Auth"],prefix='/auth')


@app.get("/")
def read_root():
    return {"Hello": "World"}