from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    pass

class UserInDB(UserBase):
    hashed_password: str

# Your other FastAPI routes can use these models
@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    # Your logic here
    return user_in

@app.get("/")
async def root():
    return {"message": "Hello World"}