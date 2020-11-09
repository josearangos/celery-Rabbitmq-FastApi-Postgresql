from fastapi import FastAPI

#Routes
from routers.user import router as userRouter
from routers.auth import router as authRouter

app = FastAPI(title="Auth Management System")


#Include routes
app.include_router(userRouter,tags=["User"],prefix='/user')
app.include_router(authRouter,tags=["Auth"],prefix='/auth')
