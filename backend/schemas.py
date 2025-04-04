from dataclasses import dataclass
from typing import Union


@dataclass
class DBUser:
    __table_name__ = "users"

    id: int
    username: str
    password: str
    is_active: bool = False
    account_balance: float = 0.0
    cells_owned: int = 0
    projects_owned: int = 0
    total_invested: float = 0.0
    total_earnings: float = 0.0
    total_energy_generated: float = 0.0
    maximum_power_generation: float = 0.0


@dataclass
class DBProject:
    __table_name__ = "projects"
    id: str
    name: str
    location_city: str
    location_country: str
    latitude: float
    longitude: float
    bidding_zone: str
    installed_capacity: str
    description: str
    number_of_cells: int
    unit_price: float
    completed_date: str | None
    is_completed: bool = False


@dataclass
class DBPanel:
    __table_name__ = "panels"
    id: str
    project_id: str
    description: str
    cell_rows: int
    cell_columns: int


@dataclass
class DBCell:
    __table_name__ = "cells"
    id: str
    owner_id: str | None
    panel_id: str
    price: float
    cell_index: int
    color: str


@dataclass
class DBUserProject:
    __table_name__ = "user_projects"
    id: str
    user_id: str
    project_id: str
    percentage_owned: float
    time_of_purchase: str


@dataclass
class DBPowerDataPoint:
    __table_name__ = "power_data"
    id: str
    project_id: str
    timestamp: str
    value: float


@dataclass
class DBEnergyDataPoint:
    __table_name__ = "energy_data"
    id: str
    project_id: str
    timestamp: str
    value: float


@dataclass
class DBEnergyPrice:
    __table_name__ = "energy_price"
    bidding_zone: str
    timestamp: str
    price: float


DBTypes = Union[
    DBUser,
    DBProject,
    DBPanel,
    DBCell,
    DBUserProject,
    DBPowerDataPoint,
    DBEnergyDataPoint,
    DBEnergyPrice,
]
