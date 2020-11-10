from fastapi import FastAPI, BackgroundTasks


#Routes
from routers.user import router as UserRouter
from routers.auth import router as AuthRouter
from routers.animal import router as AnimalRouter

app = FastAPI(title="Api GateWay Animal Management System")
app.include_router(UserRouter,tags=["User"],prefix='/user')
app.include_router(AuthRouter,tags=["Auth"],prefix='/auth')
app.include_router(AnimalRouter,tags=["Animal"],prefix='/animal')


@app.get("/")
def read_root():
    return {"Hello": "World"}

