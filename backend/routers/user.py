from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
import sqlite3
from pydantic import BaseModel
from backend.response_types import (
    UserResponse,
    UserDataResponse,
    UserStatisticsResponse,
    UserProjectResponse,
    UserPerformaceDataPointResponse,
)
from backend.routers.auth import get_user_from_token, hash_password
from backend.db_interface import DefaultDB, DBInterface
from backend.schemas import DBUser, DBUserProject
from backend.utils import multiply_elements
import uuid

router = APIRouter(prefix="/api")

CurrentUser = Annotated[UserResponse, Depends(get_user_from_token)]


def user_exists(username: str, db: DefaultDB) -> bool:
    """Check if a user exists in the database."""
    user = db.query(DBUser).filter_by(username=username).one()
    return user is not None


@router.get("/users")
async def read_users(db: DefaultDB) -> list[UserResponse]:
    users = db.query(DBUser).all()
    return [
        UserResponse(
            id=user.id,
            username=user.username,
        )
        for user in users
    ]


class UserCreationRequest(BaseModel):
    username: str
    password: str


@router.post("/users")
async def create_user(form_data: UserCreationRequest, db: DefaultDB) -> UserResponse:
    if user_exists(form_data.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    new_user = DBUser(
        id=uuid.uuid4().hex,
        username=form_data.username,
        password=hash_password(form_data.password),
        account_balance=0,
        cells_owned=0,
        projects_owned=0,
        total_invested=0,
        total_earnings=0,
        total_energy_generated=0,
        maximum_power_generation=0,
    )
    db.insert(new_user)
    return UserResponse(id=new_user.id, username=new_user.username)


@router.get("/users/{user_id}")
async def read_user(user_id: str, db: DefaultDB) -> UserResponse:
    user = db.query(DBUser).filter_by(id=user_id).one()
    return UserResponse(
        id=user.id,
        username=user.username,
    )


@router.get("/me")
async def read_users_me(user: CurrentUser) -> UserResponse:
    return user


@router.get("/me/data")
async def read_own_items(user: CurrentUser, db: DefaultDB) -> UserDataResponse:
    user_data = db.query(DBUser).filter_by(id=user.id).one()
    user_projetcts = db.query(DBUserProject).filter_by(user_id=user.id).all()

    statistics = UserStatisticsResponse(
        accountBalance=user_data.account_balance,
        cellsOwned=user_data.cells_owned,
        projectsOwned=user_data.projects_owned,
        totalInvested=user_data.total_invested,
        totalEarnings=user_data.total_earnings,
        totalEnergyGenerated=user_data.total_energy_generated,
        maximumPowerGeneration=user_data.maximum_power_generation,
    )
    projects = []
    for user_projetct in user_projetcts:
        cell_ids = fetch_owned_cells_ids(user_id=user.id, project_id=user_projetct.project_id, db=db)
        projects.append(
            UserProjectResponse(
                projectId=user_projetct.project_id,
                cellIds=cell_ids,
                percentageOwned=user_projetct.percentage_owned,
                timeOfPurchase=user_projetct.time_of_purchase,
            )
        )

    performance = fetch_user_performace(user_id=user.id, db=db)

    return UserDataResponse(
        user=user,
        statistics=statistics,
        projects=projects,
        performance=performance,
    )


def fetch_owned_cells_ids(user_id: str, project_id: str, db: DBInterface) -> list[str]:
    """Fetches the IDs of cells owned by a user in a specific project.
    Args:
        user_id (str): The ID of the user.
        project_id (str): The ID of the project.
    Returns:
        list[str]: A list of cell IDs owned by the user in the specified project."""
    with sqlite3.connect(db.db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT cells.id
            FROM cells
            JOIN panels ON cells.panel_id = panels.id
            JOIN projects ON panels.project_id = projects.id
            WHERE cells.user_id = ? AND projects.id = ?;
            """,
            (user_id, project_id),
        )
        results = cursor.fetchall()
    return [cell[0] for cell in results]


def fetch_user_performace(user_id: str, db: DBInterface) -> list[UserPerformaceDataPointResponse]:
    """Fetches the performance data points for a given user based on their project ownership.
    Args:
        user_id (str): The ID of the user.
    Returns:
        list[UserPerformaceDataPointResponse]: A list of performance data points containing timestamps and calculated values."""
    with sqlite3.connect(db.db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT 
                energy_data.timestamp AS timestamp,
                energy_data.value AS energy_value,
                energy_price.price AS energy_price,
                user_projects.percentage_owned
                
            FROM 
                user_projects
            JOIN 
                projects ON user_projects.project_id = projects.id
            JOIN 
                energy_data ON energy_data.project_id = projects.id
            JOIN 
                energy_price 
                    ON energy_price.timestamp = energy_data.timestamp 
                    AND energy_price.bidding_zone = projects.bidding_zone
            WHERE 
                user_projects.user_id = ?
                AND datetime(energy_data.timestamp) >= datetime(user_projects.time_of_purchase);

            """,
            (user_id,),
        )

        results = cursor.fetchall()

    data_points = []
    for result in results:
        timestamp, *values = result
        value = multiply_elements(values)
        data_points.append(
            UserPerformaceDataPointResponse(
                timestamp=timestamp,
                value=value,
            )
        )
    return data_points
