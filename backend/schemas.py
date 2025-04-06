from dataclasses import dataclass
from typing import Union


@dataclass
class DBUser:
    __table_name__ = "users"
    id: str = None
    username: str = ""
    password: str = ""
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
    id: str = None
    name: str = ""
    location_city: str = ""
    location_country: str = ""
    latitude: float = 0.0
    longitude: float = 0.0
    bidding_zone: str = ""
    installed_capacity: str = ""
    description: str = ""
    plant_efficiency: float = 0.0
    number_of_cells: int = 0
    unit_price: float = 0.0
    completed_date: str | None = None
    is_completed: bool = False


@dataclass
class DBPanel:
    __table_name__ = "panels"
    id: str = None
    project_id: str = ""
    description: str = ""
    cell_rows: int = 0
    cell_columns: int = 0


@dataclass
class DBCell:
    __table_name__ = "cells"
    id: str = None
    user_id: str | None = None
    panel_id: str = ""
    price: float = 0.0
    cell_index: int = 0
    color: str = "#FFFFFF"


@dataclass
class DBUserProject:
    __table_name__ = "user_projects"
    id: str = None
    user_id: str = ""
    project_id: str = ""
    percentage_owned: float = 0.0
    time_of_purchase: str = ""


@dataclass
class DBPowerDataPoint:
    __table_name__ = "power_data"
    id: str = None
    project_id: str = ""
    timestamp: str = ""
    value: float = 0.0


@dataclass
class DBEnergyDataPoint:
    __table_name__ = "energy_data"
    id: str = None
    project_id: str = ""
    timestamp: str = ""
    value: float = 0.0


@dataclass
class DBEnergyPrice:
    __table_name__ = "energy_price"
    bidding_zone: str = ""
    timestamp: str = ""
    price: float = 0.0


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
