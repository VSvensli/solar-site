# Modified example from https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
from datetime import datetime, timedelta, timezone

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi import APIRouter
from pydantic import BaseModel
from jwt.exceptions import InvalidTokenError
from backend.constants import DB_NAME
from backend.schemas import (
    DBUser,
    DBUserProject,
)
from backend.response_types import (
    UserStatisticsResponse,
    UserProjectResponse,
    UserDataResponse,
    UserPerformaceDataPointResponse,
)
from backend.db_interface import DBInterface
from backend.response_types import UserResponse

import jwt

SECRET_KEY = "16b1187d79999da9425a3f3f844b015ec4a6816b5e4c75bef8edaa168c8ad4c5"  # Dummy secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

db = DBInterface(db_name=DB_NAME)

router = APIRouter(prefix="/api")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hashed_password.partition("!")[-1] == plain_password


def hash_password(password: str) -> str:
    return "supersecret!" + password


def authenticate_user(username: str, password: str) -> UserResponse | bool:
    user = db.quary(DBUser).filter_by(username=username).one()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return UserResponse(id=user.id, username=user.username)


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
    user = authenticate_user(form_data.username, form_data.password)
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
    inactive_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Inactive user",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_not_found_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = db.quary(DBUser).filter_by(username=username).one()
    if user.disabled:
        raise inactive_exception
    if user is None:
        raise user_not_found_exception
    return user


@router.get("/me")
async def read_users_me(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> UserResponse:
    return current_user


@router.get("/me/data")
async def read_own_items(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
):
    return draft_user_data_quary(current_user.id)


def mock_user_performance_quary(user_id: str) -> list[UserPerformaceDataPointResponse]:
    mock_data = [
        {"timestamp": "2025-02-21T08:00:00Z", "value": 150.0},
        {"timestamp": "2025-02-21T08:00:00Z", "value": 170.0},
        {"timestamp": "2025-02-21T08:00:00Z", "value": 210.0},
        {"timestamp": "2025-02-21T08:00:00Z", "value": 250.0},
        {"timestamp": "2025-02-21T08:00:00Z", "value": 300.0},
        {"timestamp": "2025-02-21T08:00:00Z", "value": 380.0},
    ]
    user_performance = []
    for data in mock_data:
        user_performance.append(UserPerformaceDataPointResponse(**data))
    return user_performance


def draft_user_data_quary(user_id: str) -> UserDataResponse:
    user_projects = []
    for user_project in db.quary(DBUserProject).filter_by(user_id=user_id).all():
        user_projects.append(
            UserProjectResponse(
                projectId=user_project.project_id,
                cellIds=["1", "2", "3"],  # TODO: make a quary to find which cells are owned by the user
                percentageOwned=user_project.percentage_owned,
                timeOfPurchase=user_project.time_of_purchase,
            )
        )

    # TODO: make a quary to find/calculate the statistics
    user_statistics = {
        "accountBalance": 1000,
        "cellsOwned": 100,
        "projectsOwned": 5,
        "totalInvested": 10010,
        "totalEarnings": 1010,
        "totalEnergyGenerated": 10000,
        "maximumPowerGeneration": 1000,
    }
    user_statistics = UserStatisticsResponse(**user_statistics)
    return UserDataResponse(
        user=UserResponse(id="1", username="test"),
        statistics=user_statistics,
        projects=user_projects,
        performance=mock_user_performance_quary(user_id),
    )


if __name__ == "__main__":
    mock_user_performance_quary("s")
