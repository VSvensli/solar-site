# Modified example from https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
from datetime import datetime, timedelta, timezone

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi import APIRouter
from pydantic import BaseModel
from jwt.exceptions import InvalidTokenError

import jwt

SECRET_KEY = "16b1187d79999da9425a3f3f844b015ec4a6816b5e4c75bef8edaa168c8ad4c5"  # Dummy secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
mock_db = {
    "dev": {
        "info": {
            "id": "1",
            "name": "John Doe",
            "email": "",
        },
        "performance": [
            {"timestamp": "2021-01-01", "value": 1000},
            {"timestamp": "2021-01-02", "value": 1020},
            {"timestamp": "2021-01-03", "value": 1200},
            {"timestamp": "2021-01-04", "value": 1204},
            {"timestamp": "2021-01-05", "value": 1500},
        ],
        "statistics": {
            "accountBalance": 1000,
            "cellsOwned": 100,
            "projectsOwned": 5,
            "totalInvested": 10010,
            "totalEarnings": 1010,
            "totalEnergyGenerated": 10000,
            "maximumPowerGeneration": 1000,
        },
        "projects": [
            {
                "projectId": "CSP_FR_001",
                "cellIds": ["1", "2"],
                "percentageOwned": 0.023,
                "timeOfPurchase": "2025-02-17T03:24:00Z",
            },
            {
                "projectId": "MSP_ES_001",
                "cellIds": ["1", "2"],
                "percentageOwned": 0.5,
                "timeOfPurchase": "2024-12-17T03:24:00",
            },
            {
                "projectId": "SLG_DE_001",
                "cellIds": ["1", "2"],
                "percentageOwned": 0.01,
                "timeOfPurchase": "2024-12-17T03:24:00",
            },
        ],
    },
    "dev2": {
        "info": {
            "id": "1",
            "name": "John Doe",
            "email": "",
        },
        "performance": [
            {"timestamp": "2021-01-01", "value": 1000},
        ],
        "statistics": {
            "accountBalance": 5,
            "cellsOwned": 5,
            "projectsOwned": 2,
            "totalInvested": 10,
            "totalEarnings": 2,
            "totalEnergyGenerated": 2,
            "maximumPowerGeneration": 2,
        },
        "projects": [
            {
                "projectId": "CSP_FR_001",
                "cellIds": ["1", "2"],
                "percentageOwned": 0.001,
                "timeOfPurchase": "2025-02-17T03:24:00Z",
            },
            {
                "projectId": "MSP_ES_001",
                "cellIds": ["1", "2"],
                "percentageOwned": 0.15,
                "timeOfPurchase": "2024-12-17T03:24:00",
            },
            {
                "projectId": "SLG_DE_001",
                "cellIds": ["1", "2"],
                "percentageOwned": 0.01,
                "timeOfPurchase": "2024-12-17T03:24:00",
            },
        ],
    },
}


mock_user_database = {
    "dev": {
        "username": "dev",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "supersecret!password",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "supersecret!password",
        "disabled": True,
    },
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str) -> UserInDB | None:
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hashed_password.partition("!")[-1] == plain_password


def hash_password(password: str) -> str:
    return "supersecret!" + password


def authenticate_user(fake_db, username: str, password: str) -> UserInDB | bool:
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(mock_user_database, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(mock_user_database, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router.get("/users/me/data")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return mock_db.get(current_user.username)
