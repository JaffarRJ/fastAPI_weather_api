from fastapi import FastAPI,Depends,HTTPException,status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED
from database import Base,engine,SessionLocal
from schemas import UserRegister,UserLogin
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials # used to pass data in header 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import models
from pydantic import BaseModel
import requests
import python_weather
import asyncio
import os


Base.metadata.create_all(engine)


app=FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Settings(BaseModel):
    authjwt_secret_key:str='678cd596107563a5ec1f25e64d13380e07eac222a2d05fabf0c5d61340b86205'

    # to generate authjwt_secret_key use python secrets module
    # import secrets
    # secrets.token_hex()
    # this will generate secret_key
@AuthJWT.load_config
def get_config():
    return Settings()


# #create a user
@app.post('/signup',response_model=UserRegister,tags=['User'])
async def register(user:UserRegister,db: Session = Depends(get_db)):
    new_user=models.User(username=user.username,email=user.email,password=user.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/all_users',tags=['User'])
async def all_users(db: Session = Depends(get_db)):
    users=db.query(models.User).all()
    return users


@app.post('/login',tags=['User'])
async def login(username:str,password:str,db:Session=Depends(get_db),Authorize:AuthJWT=Depends()):
    data=db.query(models.User).filter(models.User.username == username,models.User.password==password).first()
    if data:
        access_token=Authorize.create_access_token(subject=data.username)
        refresh_token=Authorize.create_refresh_token(subject=data.username)
        username=data.username
        return {'username':username,'access_token':access_token,'refresh_token':refresh_token}
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,detail="Invalid username or password")


auth_scheme = HTTPBearer()

@app.get("/weather",tags=['Weather API'])
def get_weather(city: str,Authorize:AuthJWT=Depends(),token:HTTPAuthorizationCredentials=Depends(auth_scheme)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    api_key = "49c0bad2c7458f1c76bec9654081a661"
    api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(api_url)
    data = response.json()
    temperature=round((data["main"]["temp"]-273.15))
    return {"temperature": temperature, "description": data["weather"][0]["description"]}