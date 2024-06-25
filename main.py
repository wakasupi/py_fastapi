from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from automapper import mapper

app = FastAPI()

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class PublicUserInfo(UserBase):
    additional_info: str

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    pass

class UserInDB(UserBase):
    hashed_password: str

def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db

# Register mapping from UserBase to PublicUserInfo
mapper.add(UserBase, PublicUserInfo)

# Create a UserBase object
user_info = UserBase(username="John Malkovich", email="john@example.com")

# Map to PublicUserInfo
public_user_info = mapper.to(PublicUserInfo).map(user_info)
print(vars(public_user_info))  # {'username': 'John Malkovich', 'email': 'john@example.com'}

# Create PublicUserInfo object
public_user_info = mapper.to(PublicUserInfo).map(user_info)
print(vars(public_user_info))  # {'name': 'John Malkovich', 'profession': 'engineer'}    

@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

@app.get("/userbase")
async def root():
    return user_info

@app.get("/publicuserbase")
async def root():
    return public_user_info
