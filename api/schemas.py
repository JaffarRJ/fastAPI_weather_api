from pydantic import BaseModel


class UserRegister(BaseModel):
    #id:int
    username:str
    email:str
    password:str

    class Config:
        orm_mode=True
        schema_extra={
            "example":{
                "username":"test",
                "email":"test@gmail.com",
                "password":"password"
            }
        }

class UserLogin(BaseModel):
    username:str
    password:str

    class Config:
        orm_mode=True
