# This file contains dataclasses that are copied from the src/*.types.py files.
from pydantic import BaseModel


class UserStatistics(BaseModel):
    accountBalance: float
    cellsOwned: int
    projectsOwned: int
    totalInvested: float
    totalEarnings: float
    totalEnergyGenerated: float
    maximumPowerGeneration: float


class UserProject(BaseModel):
    projectId: str
    cellIds: list[str]
    percentageOwned: float
    timeOfPurchase: str


class UserPerformaceDataPoint(BaseModel):
    timestamp: str
    value: float


class User(BaseModel):
    id: str
    username: str


class UserData(BaseModel):
    user: User
    statistics: UserStatistics
    projects: list[UserProject]
    performance: list[UserPerformaceDataPoint]


class Project(BaseModel):
    projectId: str
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


class EnergyDataPoint(BaseModel):
    timestamp: str
    production: int


class PowerDataPoint(BaseModel):
    timestamp: str
    production: int
    isPredicted: bool


class Cell(BaseModel):
    cellId: str
    ownerId: str
    price: float
    cellIndex: int
    color: str


class Panel(BaseModel):
    projectId: str
    panelId: str
    description: str
    cellRows: int
    cellColumns: int
    cells: list[Cell] | None
