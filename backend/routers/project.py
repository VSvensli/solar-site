from ..types import Project, EnergyDataPoint, PowerDataPoint, Panel, Cell
from fastapi import APIRouter, HTTPException, status

mock_db = {
    "projects": [
        {
            "id": "1",
            "name": "Berlin Project",
            "locationCity": "Berlin",
            "locationCountry": "Germany",
            "locationBiddingZone": "DE",
            "installedCapacity": "100 MW",
            "description": "This is a project in Berlin",
            "numberOfCells": 1000,
            "unitPrice": 0.5,
            "isCompleted": True,
            "completedDate": "2021-01-01",
        },
        {
            "id": "2",
            "name": "Hamburg Project",
            "locationCity": "Hamburg",
            "locationCountry": "Germany",
            "locationBiddingZone": "DE",
            "installedCapacity": "200 MW",
            "description": "This is a project in Hamburg",
            "numberOfCells": 30403,
            "unitPrice": 0.2,
            "isCompleted": False,
            "completedDate": "2025-06-01",
        },
        {
            "id": "3",
            "name": "Oslo Project",
            "locationCity": "Oslo",
            "locationCountry": "Norway",
            "locationBiddingZone": "NO2",
            "installedCapacity": "300 MW",
            "description": "This is a project in Oslo",
            "numberOfCells": 2000,
            "unitPrice": 0.2,
            "isCompleted": True,
            "completedDate": "2023-01-01",
        },
        {
            "id": "4",
            "name": "Frankfurt Project",
            "locationCity": "Frankfurt",
            "locationCountry": "Germany",
            "locationBiddingZone": "DE",
            "installedCapacity": "400 MW",
            "description": "This is a project in Frankfurt",
            "numberOfCells": 100,
            "unitPrice": 0.5,
            "isCompleted": True,
            "completedDate": "2024-01-01",
        },
        {
            "id": "5",
            "name": "Cologne Project",
            "locationCity": "Cologne",
            "locationCountry": "Germany",
            "locationBiddingZone": "DE",
            "installedCapacity": "500 MW",
            "description": "This is a project in Cologne",
            "numberOfCells": 10,
            "unitPrice": 0.5,
            "isCompleted": True,
            "completedDate": "2025-01-01",
        },
    ],
    "energy": [
        {
            "id": "1",
            "data": [
                {"timestamp": "2025-02-21T08:00:00Z", "production": 150},
                {"timestamp": "2025-02-21T09:00:00Z", "production": 175},
                {"timestamp": "2025-02-21T10:00:00Z", "production": 200},
                {"timestamp": "2025-02-21T11:00:00Z", "production": 180},
                {"timestamp": "2025-02-21T12:00:00Z", "production": 210},
            ],
        },
        {
            "id": "2",
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
            "id": "1",
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
            "id": "2",
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
        "id": "1",
        "description": "Panel 1",
        "cellRows": 5,
        "cellColumns": 3,
        "cells": [
            {"id": "0", "ownerId": "1", "price": 0.5, "cellIndex": 0, "color": "blue"},
            {"id": "1", "ownerId": "1", "price": 0.5, "cellIndex": 1, "color": "blue"},
            {"id": "2", "ownerId": "1", "price": 0.5, "cellIndex": 2, "color": "blue"},
            {"id": "3", "ownerId": "1", "price": 0.5, "cellIndex": 3, "color": "blue"},
            {"id": "4", "ownerId": "1", "price": 0.5, "cellIndex": 4, "color": "blue"},
            {"id": "5", "ownerId": "1", "price": 0.5, "cellIndex": 5, "color": "blue"},
            {"id": "6", "ownerId": "1", "price": 0.5, "cellIndex": 6, "color": "blue"},
            {"id": "7", "ownerId": "1", "price": 0.5, "cellIndex": 7, "color": "blue"},
            {"id": "8", "ownerId": "1", "price": 0.5, "cellIndex": 8, "color": "blue"},
            {"id": "9", "ownerId": "1", "price": 0.5, "cellIndex": 9, "color": "blue"},
            {"id": "10", "ownerId": "1", "price": 0.5, "cellIndex": 10, "color": "blue"},
            {"id": "11", "ownerId": "1", "price": 0.5, "cellIndex": 11, "color": "blue"},
            {"id": "12", "ownerId": "1", "price": 0.5, "cellIndex": 12, "color": "blue"},
            {"id": "13", "ownerId": "1", "price": 0.5, "cellIndex": 13, "color": "blue"},
            {"id": "14", "ownerId": "1", "price": 0.5, "cellIndex": 14, "color": "blue"},
        ],
    },
    {
        "id": "2",
        "description": "Panel 2",
        "cellRows": 5,
        "cellColumns": 3,
        "cells": [
            {"id": "16", "ownerId": "1", "price": 0.5, "cellIndex": 0, "color": "blue"},
            {"id": "17", "ownerId": "1", "price": 0.5, "cellIndex": 1, "color": "blue"},
            {"id": "18", "ownerId": "1", "price": 0.5, "cellIndex": 2, "color": "blue"},
            {"id": "19", "ownerId": "1", "price": 0.5, "cellIndex": 3, "color": "blue"},
            {"id": "20", "ownerId": "1", "price": 0.5, "cellIndex": 4, "color": "blue"},
            {"id": "21", "ownerId": "1", "price": 0.5, "cellIndex": 5, "color": "blue"},
            {"id": "22", "ownerId": "1", "price": 0.5, "cellIndex": 6, "color": "blue"},
            {"id": "23", "ownerId": "1", "price": 0.5, "cellIndex": 7, "color": "blue"},
            {"id": "24", "ownerId": "1", "price": 0.5, "cellIndex": 8, "color": "blue"},
            {"id": "25", "ownerId": "1", "price": 0.5, "cellIndex": 9, "color": "blue"},
            {"id": "26", "ownerId": "1", "price": 0.5, "cellIndex": 10, "color": "blue"},
            {"id": "27", "ownerId": "1", "price": 0.5, "cellIndex": 11, "color": "blue"},
            {"id": "28", "ownerId": "1", "price": 0.5, "cellIndex": 12, "color": "blue"},
            {"id": "29", "ownerId": "1", "price": 0.5, "cellIndex": 13, "color": "blue"},
            {"id": "30", "ownerId": "1", "price": 0.5, "cellIndex": 14, "color": "blue"},
        ],
    },
]

router = APIRouter()


@router.get("/projects")
async def get_projects() -> list[Project]:
    return [Project(**project) for project in mock_db.get("projects")]


@router.get("/projects/{project_id}")
async def get_project(project_id: str) -> Project:
    projects = mock_db.get("projects")
    for project in projects:
        if project.get("id") == project_id:
            return Project(**project)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with project_id {project_id} not found."
    )


@router.get("/projects/{project_id}/energy")
async def get_energy_data(project_id: str) -> list[EnergyDataPoint]:
    energy_histories = mock_db.get("energy")
    for energy_history in energy_histories:
        if energy_history.get("id") == project_id:
            return [EnergyDataPoint(**data_point) for data_point in energy_history.get("data")]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Energy history for project_id {project_id} not found."
    )


@router.get("/projects/{project_id}/power")
async def get_power_data(project_id: str) -> list[PowerDataPoint]:
    power_histories = mock_db.get("power")
    for power_history in power_histories:
        if power_history.get("id") == project_id:
            return [PowerDataPoint(**data_point) for data_point in power_history.get("data")]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Power history for project_id {project_id} not found."
    )


@router.get("/projects/{project_id}/panels")
async def get_panels(project_id: str) -> list[Panel]:
    panels = mock_db.get("panels")
    for panel in panels:
        if panel.get("id") == project_id:
            cells = [Cell(**cell) for cell in panel.get("cells")]
            return Panel(
                id=panel.get("id"),
                description=panel.get("description"),
                cellRows=panel.get("cellRows"),
                cellColumns=panel.get("cellColumns"),
                cells=cells,
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Panels for project_id {project_id} not found.")
