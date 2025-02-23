# This file contains dataclasses that are copied from the src/*.types.py files.
from dataclasses import dataclass


@app.get("/projects")
def read_projects():
    return JSONResponse(content={"projects": []})


@app.get("/projects/{project_id}")
def read_project(project_id: str):
    return JSONResponse(content={"project_id": project_id})


@app.get("/projects/{project_id}/energy-data")
def read_energy_data(project_id: str):
    return JSONResponse(content={"project_id": project_id})


@app.get("/projects/{project_id}/power-data")
def read_power_data(project_id: str):
    return JSONResponse(content={"project_id": project_id})


@app.get("/projects/{project_id}/panels")
def read_panels(project_id: str):
    return JSONResponse(content={"project_id": project_id})


@dataclass
class UserStatistics:
    accountBalance: float
    cellsOwned: int
    projectsOwned: int
    totalInvested: float
    totalEarnings: float
    totalEnergyGenerated: float
    maximumPowerGeneration: float


@dataclass
class UserProject:
    projectId: str
    cellIds: list[str]
    percentageOwned: float
    timeOfPurchase: str


@dataclass
class UserPerformaceDataPoint:
    timestamp: str
    value: float


@dataclass
class User:
    id: str
    email: str
    statistics: UserStatistics
    projects: list[UserProject]


@dataclass
class Project:
    id: str
    name: str
    locationCity: str
    locationCountry: str
    locationBiddingZone: str
    installedCapacity: str
    description: str
    numberOfCells: int
    unitPrice: float
    isCompleted: bool
    completedDate: str


@dataclass
class EnergyDataPoint:
    timestamp: str
    production: int


@dataclass
class PowerDataPoint:
    timestamp: str
    production: int
    isPredicted: bool


@dataclass
class Cell:
    id: str
    ownerId: str
    price: int
    cellIndex: int
    color: str


@dataclass
class Panel:
    id: str
    description: str
    cellRows: int
    cellColumns: int
    cells: list[Cell]
