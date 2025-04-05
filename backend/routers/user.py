from fastapi import APIRouter, Depends
from typing import Annotated
import sqlite3
from backend.response_types import (
    UserResponse,
    UserDataResponse,
    UserStatisticsResponse,
    UserProjectResponse,
    UserPerformaceDataPointResponse,
)
from backend.routers.auth import get_user_from_token
from backend.db_interface import DBInterface
from backend.schemas import DBUser, DBUserProject
from backend.constants import DB_NAME
from backend.utils import multiply_elements

router = APIRouter(prefix="/api")
db = DBInterface(db_name=DB_NAME)


@router.get("/me")
async def read_users_me(
    user: Annotated[UserResponse, Depends(get_user_from_token)],
) -> UserResponse:
    return user


@router.get("/me/data")
async def read_own_items(
    user: Annotated[UserResponse, Depends(get_user_from_token)],
) -> UserDataResponse:
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
    projects = (
        [
            UserProjectResponse(
                projectId=project.id,
                cellIds=project.cell_ids,
                percentageOwned=project.percentage_owned,
                timeOfPurchase=project.time_of_purchase,
            )
            for project in user_projetcts
        ],
    )
    performance = fetch_user_performace(user.id)

    return UserDataResponse(
        user=user,
        statistics=statistics,
        projects=projects,
        performance=performance,
    )


def fetch_user_performace(user_id: str) -> list[UserPerformaceDataPointResponse]:
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


if __name__ == "__main__":
    fetch_user_performace(1)
