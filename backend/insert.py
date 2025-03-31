import sqlite3

DB_NAME = "solar.db"


def execute_query(query: str, params: tuple = ()):
    """Executes a single query with given parameters."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute(query, params)
        conn.commit()


def execute_batch_query(query: str, params_list: list[tuple]):
    """Executes a batch query with multiple records."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.executemany(query, params_list)
        conn.commit()


# Note this should be done programatically where only the row class and data is passed in
def insert_user(
    id: str,
    username: str,
    password: str,
    account_balance: float = 0.0,
    cells_owned: int = 0,
    projects_owned: int = 0,
    total_invested: float = 0.0,
    total_earnings: float = 0.0,
    total_energy_generated: float = 0.0,
    maximum_power_generation: float = 0.0,
):
    """Inserts a user into the users table."""
    query = """
    INSERT INTO users (id, username, password, account_balance, cells_owned, projects_owned, total_invested, 
                       total_earnings, total_energy_generated, maximum_power_generation)
    VALUES (?, ?, ?, ?, ?, ?, ?,?, ?, ?);
    """
    execute_query(
        query,
        (
            id,
            username,
            password,
            account_balance,
            cells_owned,
            projects_owned,
            total_invested,
            total_earnings,
            total_energy_generated,
            maximum_power_generation,
        ),
    )


def insert_project(
    project_id: str,
    name: str,
    location_city: str,
    location_country: str,
    latitude: float,
    longitude: float,
    bidding_zone: str,
    installed_capacity: str,
    description: str,
    number_of_cells: int,
    unit_price: float,
    is_completed: bool = False,
    completed_date: str | None = None,
):
    """Inserts a project into the projects table."""
    query = """
    INSERT INTO projects (project_id, name, location_city, location_country, latitude, longitude,
                          bidding_zone, installed_capacity, description, number_of_cells, unit_price, is_completed, completed_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    execute_query(
        query,
        (
            project_id,
            name,
            location_city,
            location_country,
            latitude,
            longitude,
            bidding_zone,
            installed_capacity,
            description,
            number_of_cells,
            unit_price,
            is_completed,
            completed_date,
        ),
    )


def insert_panel(panel_id: str, project_id: str, description: str, cell_rows: int, cell_columns: int):
    """Inserts a panel into the panels table."""
    query = """
    INSERT INTO panels (panel_id, project_id, description, cell_rows, cell_columns)
    VALUES (?, ?, ?, ?, ?);
    """
    execute_query(query, (panel_id, project_id, description, cell_rows, cell_columns))


def insert_cell(cell_id: str, owner_id: str | None, panel_id: str, price: float, cell_index: int, color: str):
    """Inserts a cell into the Cclls table."""
    query = """
    INSERT INTO cells (cell_id, owner_id, panel_id, price, cell_index, color)
    VALUES (?, ?, ?, ?, ?, ?);
    """
    execute_query(query, (cell_id, owner_id, panel_id, price, cell_index, color))


def insert_user_project(user_id: str, project_id: str, percentage_owned: float, time_of_purchase: str):
    """Inserts a user-project relationship into the user_projects table."""
    query = """
    INSERT INTO user_projects (user_id, project_id, percentage_owned, time_of_purchase)
    VALUES (?, ?, ?, ?);
    """
    execute_query(query, (user_id, project_id, percentage_owned, time_of_purchase))


def insert_energy_data_point(project_id: str, timestamp: str, value: float):
    """Inserts an energy metric into the energy_data table."""
    query = """
    INSERT INTO energy_data (project_id, timestamp, value)
    VALUES (?, ?, ?);
    """
    execute_query(query, (project_id, timestamp, value))


def insert_power_data_point(project_id: str, timestamp: str, value: float):
    """Inserts an energy metric into the power_data table."""
    query = """
    INSERT INTO power_data (project_id, timestamp, value)
    VALUES (?, ?, ?);
    """
    execute_query(query, (project_id, timestamp, value))


def insert_energy_price(bidding_zone: str, timestamp: str, price: float):
    """Inserts an energy price data point into the energy_price table."""
    query = """
    INSERT INTO energy_price (bidding_zone, timestamp, price)
    VALUES (?, ?, ?);
    """
    execute_query(query, (bidding_zone, timestamp, price))


def batch_insert_cells(cells: list[tuple[str, str | None, str, float, int, str]]):
    """Inserts multiple cells into the cells table."""
    query = """
    INSERT INTO cells (cell_id, owner_id, panel_id, price, cell_index, color)
    VALUES (?, ?, ?, ?, ?, ?);
    """
    execute_batch_query(query, cells)


# def batch_insert_energy_data_points(data_points: list[tuple[str, str, str, float]]):
#     """Inserts multiple energy metrics into the EnergyMetrics table."""
#     query = """
#     INSERT INTO energy_metrics (project_id, timestamp, metric_type, value)
#     VALUES (?, ?, ?, ?);
#     """
#     execute_batch_query(query, data_points)


# def batch_insert_energy_prices(prices: list[tuple[str, str, float]]):
#     """Inserts multiple energy price data points."""
#     query = """
#     INSERT INTO EnergyPriceTimeSeries (biddingZone, timestamp, price)
#     VALUES (?, ?, ?);
#     """
#     execute_batch_query(query, prices)
