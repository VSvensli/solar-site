from ..types import Project, EnergyDataPoint, PowerDataPoint, Panel, Cell
from fastapi import APIRouter, HTTPException, status


# Instance for Cestas Solar Park, France
project1 = Project(
    projectId="CSP_FR_001",
    name="Cestas Solar Park",
    locationCity="Cestas",
    locationCountry="France",
    locationBiddingZone="FR",
    installedCapacity="300 MW",
    description=(
        "Located near Bordeaux in the Nouvelle-Aquitaine region, Cestas Solar Park is one of Europe’s largest "
        "photovoltaic installations. Commissioned in 2015 with a capacity of approximately 300 MW and covering "
        "over 260 hectares, the facility employs advanced PV modules to convert abundant sunlight into electricity. "
        "It significantly contributes to France’s renewable energy targets and supplies clean power to tens of thousands "
        "of households."
    ),
    numberOfCells=1000000,  # Estimated based on typical panel capacity
    unitPrice=2.50,  # Assumed unit price per cell in EUR
    isCompleted=True,
    completedDate="2015-01-01",
)

# Instance for Mula Solar Power Plant, Spain
project2 = Project(
    projectId="MSP_ES_001",
    name="Mula Solar Power Plant",
    locationCity="Mula",
    locationCountry="Spain",
    locationBiddingZone="ES",
    installedCapacity="60 MW",
    description=(
        "Situated in the sunny Murcia region, the Mula Solar Power Plant harnesses the area’s high solar irradiance to "
        "generate renewable energy. With an installed capacity of around 60 MW, this project uses state-of-the-art "
        "photovoltaic technology over a sprawling open area. Commissioned in the mid-2010s, it plays an important role "
        "in Spain’s drive toward sustainable energy production and reducing carbon emissions."
    ),
    numberOfCells=200000,  # Estimated based on typical panel capacity
    unitPrice=2.30,  # Assumed unit price per cell in EUR
    isCompleted=True,
    completedDate="2016-01-01",
)

# Instance for Solarpark Lieberose, Germany
project3 = Project(
    projectId="SLG_DE_001",
    name="Solarpark Lieberose",
    locationCity="Lieberose",
    locationCountry="Germany",
    locationBiddingZone="DE",
    installedCapacity="70 MW",
    description=(
        "Located in Brandenburg near the town of Lieberose, Solarpark Lieberose is a pioneering photovoltaic installation "
        "in Germany. With a capacity of roughly 70 MW, the project was among the early large-scale PV deployments in the region, "
        "demonstrating solar energy’s viability in northern European climates. Its expansive array of solar panels contributes "
        "clean energy to Germany’s grid and supports the nation’s renewable portfolio."
    ),
    numberOfCells=233333,  # Estimated based on typical panel capacity
    unitPrice=2.40,  # Assumed unit price per cell in EUR
    isCompleted=True,
    completedDate="2011-01-01",
)

# Instance for Shotwick Solar Park, United Kingdom
project4 = Project(
    projectId="SSP_UK_001",
    name="Shotwick Solar Park",
    locationCity="Shotwick",
    locationCountry="United Kingdom",
    locationBiddingZone="UK",
    installedCapacity="72 MW",
    description=(
        "Positioned in Cheshire, England, Shotwick Solar Park stands as one of the largest solar farms in the United Kingdom. "
        "Boasting an installed capacity of about 72 MW and spanning several hundred acres, it features thousands of high-efficiency "
        "solar panels. Commissioned in the late 2010s, the facility supplies renewable electricity to the local grid, aiding the UK’s "
        "transition from fossil fuels and lowering carbon emissions."
    ),
    numberOfCells=240000,  # Estimated based on typical panel capacity
    unitPrice=2.35,  # Assumed unit price per cell in EUR
    isCompleted=True,
    completedDate="2018-01-01",
)

# Instance for Catania Solar Park, Italy
project5 = Project(
    projectId="CSP_IT_001",
    name="Catania Solar Park",
    locationCity="Catania",
    locationCountry="Italy",
    locationBiddingZone="IT",
    installedCapacity="50 MW",
    description=(
        "Located near Catania in Sicily, the Catania Solar Park capitalizes on the Mediterranean’s abundant sunshine to produce "
        "renewable energy. With a capacity of approximately 50 MW, this photovoltaic project has been operational since the late "
        "2010s and occupies an extensive site in one of Italy’s sunniest regions. It plays a crucial role in boosting Italy’s renewable "
        "energy capacity and reducing reliance on conventional fossil fuel sources."
    ),
    numberOfCells=166667,  # Estimated based on typical panel capacity
    unitPrice=2.20,  # Assumed unit price per cell in EUR
    isCompleted=True,
    completedDate="2019-01-01",
)


mock_db = {
    "projects": [
        {
            "projectId": project1.projectId,
            "name": project1.name,
            "locationCity": project1.locationCity,
            "locationCountry": project1.locationCountry,
            "locationBiddingZone": project1.locationBiddingZone,
            "installedCapacity": project1.installedCapacity,
            "description": project1.description,
            "numberOfCells": project1.numberOfCells,
            "unitPrice": project1.unitPrice,
            "isCompleted": project1.isCompleted,
            "completedDate": project1.completedDate,
        },
        {
            "projectId": project2.projectId,
            "name": project2.name,
            "locationCity": project2.locationCity,
            "locationCountry": project2.locationCountry,
            "locationBiddingZone": project2.locationBiddingZone,
            "installedCapacity": project2.installedCapacity,
            "description": project2.description,
            "numberOfCells": project2.numberOfCells,
            "unitPrice": project2.unitPrice,
            "isCompleted": project2.isCompleted,
            "completedDate": project2.completedDate,
        },
        {
            "projectId": project3.projectId,
            "name": project3.name,
            "locationCity": project3.locationCity,
            "locationCountry": project3.locationCountry,
            "locationBiddingZone": project3.locationBiddingZone,
            "installedCapacity": project3.installedCapacity,
            "description": project3.description,
            "numberOfCells": project3.numberOfCells,
            "unitPrice": project3.unitPrice,
            "isCompleted": project3.isCompleted,
            "completedDate": project3.completedDate,
        },
        {
            "projectId": project4.projectId,
            "name": project4.name,
            "locationCity": project4.locationCity,
            "locationCountry": project4.locationCountry,
            "locationBiddingZone": project4.locationBiddingZone,
            "installedCapacity": project4.installedCapacity,
            "description": project4.description,
            "numberOfCells": project4.numberOfCells,
            "unitPrice": project4.unitPrice,
            "isCompleted": project4.isCompleted,
            "completedDate": project4.completedDate,
        },
        {
            "projectId": project5.projectId,
            "name": project5.name,
            "locationCity": project5.locationCity,
            "locationCountry": project5.locationCountry,
            "locationBiddingZone": project5.locationBiddingZone,
            "installedCapacity": project5.installedCapacity,
            "description": project5.description,
            "numberOfCells": project5.numberOfCells,
            "unitPrice": project5.unitPrice,
            "isCompleted": project5.isCompleted,
            "completedDate": project5.completedDate,
        },
    ],
    "energy": [
        {
            "projectId": project1.projectId,
            "data": [
                {"timestamp": "2025-02-21T08:00:00Z", "production": 150},
                {"timestamp": "2025-02-21T09:00:00Z", "production": 175},
                {"timestamp": "2025-02-21T10:00:00Z", "production": 200},
                {"timestamp": "2025-02-21T11:00:00Z", "production": 180},
                {"timestamp": "2025-02-21T12:00:00Z", "production": 210},
            ],
        },
        {
            "projectId": "2",
            "data": [
                {"timestamp": "2025-02-21T08:00:00Z", "production": 250},
                {"timestamp": "2025-02-21T09:00:00Z", "production": 275},
                {"timestamp": "2025-02-21T10:00:00Z", "production": 200},
                {"timestamp": "2025-02-21T11:00:00Z", "production": 280},
                {"timestamp": "2025-02-21T12:00:00Z", "production": 210},
            ],
        },
    ],
    "power": [
        {
            "projectId": project1.projectId,
            "data": [
                {"timestamp": "2025-02-21T08:00:00Z", "production": 150, "isPredicted": False},
                {"timestamp": "2025-02-21T09:00:00Z", "production": 175, "isPredicted": False},
                {"timestamp": "2025-02-21T10:00:00Z", "production": 200, "isPredicted": False},
                {"timestamp": "2025-02-21T11:00:00Z", "production": 180, "isPredicted": False},
                {"timestamp": "2025-02-21T12:00:00Z", "production": 210, "isPredicted": False},
                {"timestamp": "2025-02-21T13:00:00Z", "production": 300, "isPredicted": False},
                {"timestamp": "2025-02-21T14:00:00Z", "production": 220, "isPredicted": True},
                {"timestamp": "2025-02-21T15:00:00Z", "production": 200, "isPredicted": True},
                {"timestamp": "2025-02-21T16:00:00Z", "production": 180, "isPredicted": True},
                {"timestamp": "2025-02-21T17:00:00Z", "production": 100, "isPredicted": True},
            ],
        },
        {
            "projectId": project2.projectId,
            "data": [
                {"timestamp": "2025-02-21T08:00:00Z", "production": 350, "isPredicted": False},
                {"timestamp": "2025-02-21T09:00:00Z", "production": 375, "isPredicted": False},
                {"timestamp": "2025-02-21T10:00:00Z", "production": 300, "isPredicted": False},
                {"timestamp": "2025-02-21T11:00:00Z", "production": 380, "isPredicted": False},
                {"timestamp": "2025-02-21T12:00:00Z", "production": 310, "isPredicted": False},
                {"timestamp": "2025-02-21T13:00:00Z", "production": 300, "isPredicted": False},
                {"timestamp": "2025-02-21T14:00:00Z", "production": 320, "isPredicted": True},
                {"timestamp": "2025-02-21T15:00:00Z", "production": 300, "isPredicted": True},
                {"timestamp": "2025-02-21T16:00:00Z", "production": 380, "isPredicted": True},
                {"timestamp": "2025-02-21T17:00:00Z", "production": 300, "isPredicted": True},
            ],
        },
    ],
}

mock_db["panels"] = [
    {
        "projectId": project1.projectId,
        "panelId": "1",
        "description": "Panel 1",
        "cellRows": 5,
        "cellColumns": 3,
        "cells": [
            {"cellId": "0", "ownerId": "1", "price": 0.5, "cellIndex": 0, "color": "blue"},
            {"cellId": "1", "ownerId": "1", "price": 0.5, "cellIndex": 1, "color": "blue"},
            {"cellId": "2", "ownerId": "1", "price": 0.5, "cellIndex": 2, "color": "blue"},
            {"cellId": "3", "ownerId": "1", "price": 0.5, "cellIndex": 3, "color": "blue"},
            {"cellId": "4", "ownerId": "1", "price": 0.5, "cellIndex": 4, "color": "blue"},
            {"cellId": "5", "ownerId": "1", "price": 0.5, "cellIndex": 5, "color": "blue"},
            {"cellId": "6", "ownerId": "1", "price": 0.5, "cellIndex": 6, "color": "blue"},
            {"cellId": "7", "ownerId": "1", "price": 0.5, "cellIndex": 7, "color": "blue"},
            {"cellId": "8", "ownerId": "1", "price": 0.5, "cellIndex": 8, "color": "blue"},
            {"cellId": "9", "ownerId": "1", "price": 0.5, "cellIndex": 9, "color": "blue"},
            {"cellId": "10", "ownerId": "1", "price": 0.5, "cellIndex": 10, "color": "blue"},
            {"cellId": "11", "ownerId": "1", "price": 0.5, "cellIndex": 11, "color": "blue"},
            {"cellId": "12", "ownerId": "1", "price": 0.5, "cellIndex": 12, "color": "blue"},
            {"cellId": "13", "ownerId": "1", "price": 0.5, "cellIndex": 13, "color": "blue"},
            {"cellId": "14", "ownerId": "1", "price": 0.5, "cellIndex": 14, "color": "blue"},
        ],
    },
    {
        "projectId": project2.projectId,
        "panelId": "2",
        "description": "Panel 2",
        "cellRows": 5,
        "cellColumns": 3,
        "cells": [
            {"cellId": "16", "ownerId": "1", "price": 0.5, "cellIndex": 0, "color": "blue"},
            {"cellId": "17", "ownerId": "1", "price": 0.5, "cellIndex": 1, "color": "blue"},
            {"cellId": "18", "ownerId": "1", "price": 0.5, "cellIndex": 2, "color": "blue"},
            {"cellId": "19", "ownerId": "1", "price": 0.5, "cellIndex": 3, "color": "blue"},
            {"cellId": "20", "ownerId": "1", "price": 0.5, "cellIndex": 4, "color": "blue"},
            {"cellId": "21", "ownerId": "1", "price": 0.5, "cellIndex": 5, "color": "blue"},
            {"cellId": "22", "ownerId": "1", "price": 0.5, "cellIndex": 6, "color": "blue"},
            {"cellId": "23", "ownerId": "1", "price": 0.5, "cellIndex": 7, "color": "blue"},
            {"cellId": "24", "ownerId": "1", "price": 0.5, "cellIndex": 8, "color": "blue"},
            {"cellId": "25", "ownerId": "1", "price": 0.5, "cellIndex": 9, "color": "blue"},
            {"cellId": "26", "ownerId": "1", "price": 0.5, "cellIndex": 10, "color": "blue"},
            {"cellId": "27", "ownerId": "1", "price": 0.5, "cellIndex": 11, "color": "blue"},
            {"cellId": "28", "ownerId": "1", "price": 0.5, "cellIndex": 12, "color": "blue"},
            {"cellId": "29", "ownerId": "1", "price": 0.5, "cellIndex": 13, "color": "blue"},
            {"cellId": "30", "ownerId": "1", "price": 0.5, "cellIndex": 14, "color": "blue"},
        ],
    },
    {
        "projectId": project2.projectId,
        "panelId": "3",
        "description": "Panel 3",
        "cellRows": 5,
        "cellColumns": 3,
        "cells": [
            {"cellId": "31", "ownerId": "1", "price": 0.5, "cellIndex": 0, "color": "blue"},
            {"cellId": "32", "ownerId": "1", "price": 0.5, "cellIndex": 1, "color": "blue"},
            {"cellId": "33", "ownerId": "1", "price": 0.5, "cellIndex": 2, "color": "blue"},
            {"cellId": "34", "ownerId": "1", "price": 0.5, "cellIndex": 3, "color": "blue"},
            {"cellId": "35", "ownerId": "1", "price": 0.5, "cellIndex": 4, "color": "blue"},
            {"cellId": "36", "ownerId": "1", "price": 0.5, "cellIndex": 5, "color": "blue"},
            {"cellId": "37", "ownerId": "1", "price": 0.5, "cellIndex": 6, "color": "blue"},
            {"cellId": "38", "ownerId": "1", "price": 0.5, "cellIndex": 7, "color": "blue"},
            {"cellId": "39", "ownerId": "1", "price": 0.5, "cellIndex": 8, "color": "blue"},
            {"cellId": "40", "ownerId": "1", "price": 0.5, "cellIndex": 9, "color": "blue"},
            {"cellId": "41", "ownerId": "1", "price": 0.5, "cellIndex": 10, "color": "blue"},
            {"cellId": "42", "ownerId": "1", "price": 0.5, "cellIndex": 11, "color": "blue"},
            {"cellId": "43", "ownerId": "1", "price": 0.5, "cellIndex": 12, "color": "blue"},
            {"cellId": "44", "ownerId": "1", "price": 0.5, "cellIndex": 13, "color": "blue"},
            {"cellId": "45", "ownerId": "1", "price": 0.5, "cellIndex": 14, "color": "blue"},
        ],
    },
]

router = APIRouter(prefix="/api")


@router.get("/projects")
async def get_projects() -> list[Project]:
    return [Project(**project) for project in mock_db.get("projects")]


@router.get("/projects/{project_id}")
async def get_project(project_id: str) -> Project:
    projects = mock_db.get("projects")
    for project in projects:
        if project.get("projectId") == project_id:
            return Project(**project)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with project_id {project_id} not found."
    )


@router.get("/projects/{project_id}/energy")
async def get_energy_data(project_id: str) -> list[EnergyDataPoint]:
    energy_histories = mock_db.get("energy")
    for energy_history in energy_histories:
        if energy_history.get("projectId") == project_id:
            return [EnergyDataPoint(**data_point) for data_point in energy_history.get("data")]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Energy history for project_id {project_id} not found."
    )


@router.get("/projects/{project_id}/power")
async def get_power_data(project_id: str) -> list[PowerDataPoint]:
    power_histories = mock_db.get("power")
    for power_history in power_histories:
        if power_history.get("projectId") == project_id:
            return [PowerDataPoint(**data_point) for data_point in power_history.get("data")]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Power history for project_id {project_id} not found."
    )


@router.get("/projects/{project_id}/panels")
async def get_panels(project_id: str) -> list[Panel]:
    panels = mock_db.get("panels")
    resp = []
    for panel in panels:
        if panel.get("projectId") == project_id:
            cells = [Cell(**cell) for cell in panel.get("cells")]
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
