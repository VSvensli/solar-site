# This file contains dataclasses that are copied from the src/*.types.py files.
from pydantic import BaseModel


class UserStatisticsResponse(BaseModel):
    accountBalance: float
    cellsOwned: int
    projectsOwned: int
    totalInvested: float
    totalEarnings: float
    totalEnergyGenerated: float
    maximumPowerGeneration: float


class UserProjectResponse(BaseModel):
    projectId: str
    cellIds: list[str]
    percentageOwned: float
    timeOfPurchase: str


class UserPerformaceDataPointResponse(BaseModel):
    timestamp: str
    value: float


class UserResponse(BaseModel):
    id: str
    username: str


class UserDataResponse(BaseModel):
    user: UserResponse
    statistics: UserStatisticsResponse
    projects: list[UserProjectResponse]
    performance: list[UserPerformaceDataPointResponse]


class ProjectResponse(BaseModel):
    projectId: str
    name: str
    locationCity: str
    locationCountry: str
    locationLatitude: float
    locationLongitude: float
    locationBiddingZone: str
    installedCapacity: str
    description: str
    numberOfCells: int
    unitPrice: float
    isCompleted: bool
    completedDate: str


class PowerPriceDataPointResponse(BaseModel):
    timestamp: str
    price: float


class EnergyDataPointResponse(BaseModel):
    timestamp: str
    production: int


class PowerDataPointResponse(BaseModel):
    timestamp: str
    production: int
    isPredicted: bool


class CellResponse(BaseModel):
    cellId: str
    userId: str
    price: float
    cellIndex: int
    color: str


class PanelResponse(BaseModel):
    projectId: str
    panelId: str
    description: str
    cellRows: int
    cellColumns: int
    cells: list[CellResponse] | None
