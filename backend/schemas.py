from dataclasses import dataclass


@dataclass
class UserRow:
    id: str
    email: str
    account_balance: float = 0.0
    cells_owned: int = 0
    projects_owned: int = 0
    total_invested: float = 0.0
    total_earnings: float = 0.0
    total_energy_generated: float = 0.0
    maximum_power_generation: float = 0.0


@dataclass
class ProjectRow:
    project_id: str
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
class PanelRow:
    panel_id: str
    project_id: str
    description: str
    cell_rows: int
    cell_columns: int


@dataclass
class CellRow:
    cell_id: str
    owner_id: str | None
    panel_id: str
    price: float
    cell_index: int
    color: str


@dataclass
class UserProjectRow:
    user_id: str
    project_id: str
    percentage_owned: float
    time_of_purchase: str


@dataclass
class PowerDataPointRow:
    project_id: str
    timestamp: str
    value: float


@dataclass
class EnergyDataPointRow:
    project_id: str
    timestamp: str
    value: float


@dataclass
class EnergyPriceRow:
    bidding_zone: str
    timestamp: str
    price: float
