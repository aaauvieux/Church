from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from schema.user_schema import UserSchema, DataUser
from model.users import users
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List
from config.db import engine
import os
from dotenv import load_dotenv

load_dotenv()
imagedir = os.getenv('IMAGEDIR')

user = APIRouter()

@user.get("/")
def root():
    return {"message": "Hi, I am FastAPI with a router"}

@user.get("/api/user", response_model=List[UserSchema])
def get_users():
    with engine.connect() as conn:
        result = conn.execute(users.select()).fetchall()
        
        return result

@user.get("/api/user/{user_id}", response_model=UserSchema)
def get_user(user_id: str):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.id == user_id)).first()
        
        return result

@user.post("/api/user", status_code=HTTP_201_CREATED)
def create_user(data_user: UserSchema):
    with engine.connect() as conn:
        new_user = data_user.dict()
        new_user["user_passw"] = generate_password_hash(data_user.user_passw, "pbkdf2:sha256:30", 30)
        new_user["image"] = f"{imagedir}{data_user.image}"
        conn.execute(users.insert().values(new_user))
        
        return Response(status_code=HTTP_201_CREATED)

@user.post("/api/user/login", status_code=200)
def user_login(data_user: DataUser):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.username == data_user.username)).first()
        if result != None:
            check_passw = check_password_hash(result[3], data_user.user_passw )
            if check_passw:
                return {
                    "Status": 200,
                    "message": "Access success"
                }    
        return {
            "Status": HTTP_401_UNAUTHORIZED,
            "message": "Access denied"
             }
    
@user.put("/api/user/{user_id}", response_model=UserSchema)
def update_user(data_update: UserSchema, user_id: str):
    with engine.connect() as conn:
        encryp_passw = generate_password_hash(data_update.user_passw, "pbkdf2:sha256:30", 30)
        new_image = f"{imagedir}{data_update.image}"
        conn.execute(users.update().values(name=data_update.name, username=data_update.username, user_passw=encryp_passw, image=new_image).where(users.c.id == user_id))
        
        result = conn.execute(users.select().where(users.c.id == user_id)).first()
        
        return result

@user.delete("/api/user/{user_id}", status_code=HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    with engine.connect() as conn:
       
        conn.execute(users.delete().where(users.c.id == user_id))
        
        return Response(status_code=HTTP_204_NO_CONTENT)
