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
    email: str
    statistics: UserStatistics
    projects: list[UserProject]


class Project(BaseModel):
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


class EnergyDataPoint(BaseModel):
    timestamp: str
    production: int


class PowerDataPoint(BaseModel):
    timestamp: str
    production: int
    isPredicted: bool


class Cell(BaseModel):
    id: str
    ownerId: str
    price: int
    cellIndex: int
    color: str


class Panel(BaseModel):
    id: str
    description: str
    cellRows: int
    cellColumns: int
    cells: list[Cell]
