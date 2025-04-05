import datetime

from fastapi import APIRouter, HTTPException, status

from backend.constants import DB_NAME
from backend.db_interface import DBInterface
from backend.response_types import (
    CellResponse,
    EnergyDataPointResponse,
    PanelResponse,
    PowerDataPointResponse,
    ProjectResponse,
)
from backend.schemas import (
    DBCell,
    DBEnergyDataPoint,
    DBPanel,
    DBPowerDataPoint,
    DBProject,
)

router = APIRouter(prefix="/api")
db = DBInterface(db_name=DB_NAME)


@router.get("/projects")
async def get_projects() -> list[ProjectResponse]:
    projects = []
    for project in db.query(DBProject).all():
        projects.append(
            ProjectResponse(
                projectId=project.id,
                name=project.name,
                locationCity=project.location_city,
                locationCountry=project.location_country,
                locationLatitude=project.longitude,
                locationLongitude=project.longitude,
                locationBiddingZone=project.bidding_zone,
                installedCapacity=project.installed_capacity,
                description=project.description,
                numberOfCells=project.number_of_cells,
                unitPrice=project.unit_price,
                isCompleted=project.is_completed,
                completedDate=project.completed_date,
            )
        )
    if projects:
        return projects
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No projects found.")


@router.get("/projects/{project_id}")
async def get_project(project_id: str) -> ProjectResponse:
    project = db.query(DBProject).filter_by(id=project_id).one()
    if project:
        return ProjectResponse(
            projectId=project.id,
            name=project.name,
            locationCity=project.location_city,
            locationCountry=project.location_country,
            locationLatitude=project.longitude,
            locationLongitude=project.longitude,
            locationBiddingZone=project.bidding_zone,
            installedCapacity=project.installed_capacity,
            description=project.description,
            numberOfCells=project.number_of_cells,
            unitPrice=project.unit_price,
            isCompleted=project.is_completed,
            completedDate=project.completed_date,
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Project with project_id {project_id} not found.",
    )


@router.get("/projects/{project_id}/energy")
async def get_energy_data(project_id: str) -> list[EnergyDataPointResponse]:
    data_points = []
    for data_point in db.query(DBEnergyDataPoint).filter_by(project_id=project_id).all():
        data_points.append(
            EnergyDataPointResponse(
                timestamp=data_point.timestamp,
                production=data_point.value,
            )
        )
    if data_points:
        return data_points
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Energy history for project_id {project_id} not found.",
    )


def is_data_point_predicted(data_point: DBPowerDataPoint) -> bool:
    return datetime.datetime.strptime(data_point.timestamp, "%Y-%m-%dT%H:%M:%SZ") > datetime.datetime.now()


@router.get("/projects/{project_id}/power")
async def get_power_data(project_id: str) -> list[PowerDataPointResponse]:
    data_points = []
    for data_point in db.query(DBPowerDataPoint).filter_by(project_id=project_id).all():
        data_points.append(
            PowerDataPointResponse(
                timestamp=data_point.timestamp,
                production=data_point.value,
                isPredicted=is_data_point_predicted(data_point),
            )
        )
    if data_points:
        return data_points
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Power history for project_id {project_id} not found.",
    )


@router.get("/projects/{project_id}/panels")
async def get_panels(project_id: str) -> list[PanelResponse]:
    panels = []
    for panel in db.query(DBPanel).filter_by(project_id=project_id).all():
        cells = []
        for cell in db.query(DBCell).filter_by(panel_id=panel.id).all():
            cells.append(
                CellResponse(
                    cellId=cell.id,
                    userId=cell.user_id,
                    panelId=cell.panel_id,
                    price=cell.price,
                    cellIndex=cell.cell_index,
                    color=cell.color,
                )
            )
        panels.append(
            PanelResponse(
                panelId=panel.id,
                projectId=panel.project_id,
                description=panel.description,
                cellRows=panel.cell_rows,
                cellColumns=panel.cell_columns,
                cells=cells,
            )
        )
    if panels:
        return panels
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Panels for project_id {project_id} not found.",
    )
