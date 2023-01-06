from sqlalchemy import Column,String,Integer,ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):

    __tablename__='users'
    id = Column(Integer, primary_key=True, index=True)
    username=Column(String,unique=True,index=True)
    email=Column(String,unique=True)
    password=Column(String)

    def __repr__(self):
        return f'<{self.username}--{self.email}'
