from backend.request_types import Project, EnergyDataPoint, PowerDataPoint, Panel, Cell
import backend.query as query
from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/api")


@router.get("/projects")
async def get_projects() -> list[Project]:
    return [Project(**project) for project in query.get_all_projects()]


@router.get("/projects/{project_id}")
async def get_project(project_id: str) -> Project:
    project = query.get_project(project_id)
    if project:
        return Project(**project)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with project_id {project_id} not found."
    )


@router.get("/projects/{project_id}/energy")
async def get_energy_data(project_id: str) -> list[EnergyDataPoint]:
    energy_histories = query.get_all_energy_data(project_id)
    for energy_history in energy_histories:
        if energy_history.get("projectId") == project_id:
            return [EnergyDataPoint(**data_point) for data_point in energy_history.get("data")]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Energy history for project_id {project_id} not found."
    )


@router.get("/projects/{project_id}/power")
async def get_power_data(project_id: str) -> list[PowerDataPoint]:
    power_histories = query.get_all_power_data(project_id)
    for power_history in power_histories:
        if power_history.get("projectId") == project_id:
            return [PowerDataPoint(**data_point) for data_point in power_history.get("data")]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Power history for project_id {project_id} not found."
    )


@router.get("/projects/{project_id}/panels")
async def get_panels(project_id: str) -> list[Panel]:
    panels = query.get_project_panels(project_id)
    resp = []
    for panel in panels:
        cells = [Cell(**cell) for cell in query.get_project_cells(panel.get("panelId"))]
        resp.append(
            Panel(
                projectId=panel.get("projectId"),
                panelId=panel.get("panelId"),
                description=panel.get("description"),
                cellRows=panel.get("cellRows"),
                cellColumns=panel.get("cellColumns"),
                cells=cells,
            )
        )
    if not resp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Panels for project_id {project_id} not found."
        )
    return resp
