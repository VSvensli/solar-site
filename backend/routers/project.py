from backend.request_types import Project, EnergyDataPoint, PowerDataPoint, Panel, Cell
from backend.schemas import PowerDataPointRow
import backend.query as query
from fastapi import APIRouter, HTTPException, status
import datetime

router = APIRouter(prefix="/api")


@router.get("/projects")
async def get_projects() -> list[Project]:
    projects = []
    for project in query.get_all_projects():
        projects.append(
            Project(
                projectId=project.project_id,
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
async def get_project(project_id: str) -> Project:
    project = query.get_project(project_id)
    if project:
        return Project(
            projectId=project.project_id,
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
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with project_id {project_id} not found."
    )


@router.get("/projects/{project_id}/energy")
async def get_energy_data(project_id: str) -> list[EnergyDataPoint]:
    data_points = []
    for data_point in query.get_all_energy_data(project_id):
        data_points.append(
            EnergyDataPoint(
                timestamp=data_point.timestamp,
                production=data_point.value,
            )
        )
    if data_points:
        return data_points
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Energy history for project_id {project_id} not found."
    )


# TODO: Move to prossesing.py
def is_data_point_predicted(data_point: PowerDataPointRow) -> bool:
    return datetime.datetime.strptime(data_point.timestamp, "%Y-%m-%dT%H:%M:%SZ") > datetime.datetime.now()


@router.get("/projects/{project_id}/power")
async def get_power_data(project_id: str) -> list[PowerDataPoint]:
    data_points = []
    for data_point in query.get_all_power_data(project_id):
        data_points.append(
            PowerDataPoint(
                timestamp=data_point.timestamp,
                production=data_point.value,
                isPredicted=is_data_point_predicted(data_point),
            )
        )
    if data_points:
        return data_points
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Power history for project_id {project_id} not found."
    )


@router.get("/projects/{project_id}/panels")
async def get_panels(project_id: str) -> list[Panel]:
    panels = []
    for panel in query.get_project_panels(project_id):
        cells = []
        for cell in query.get_project_cells(panel_id=panel.panel_id):
            cells.append(
                Cell(
                    cellId=cell.cell_id,
                    ownerId=cell.owner_id,
                    panelId=cell.panel_id,
                    price=cell.price,
                    cellIndex=cell.cell_index,
                    color=cell.color,
                )
            )
        panels.append(
            Panel(
                projectId=panel.project_id,
                panelId=panel.panel_id,
                description=panel.description,
                cellRows=panel.cell_rows,
                cellColumns=panel.cell_columns,
                cells=cells,
            )
        )
    if panels:
        return panels
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Panels for project_id {project_id} not found.")
