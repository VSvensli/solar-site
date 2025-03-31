import sqlite3
from backend.schemas import (
    DBProject,
    DBPanel,
    DBCell,
    DBEnergyDataPoint,
    DBPowerDataPoint,
    DBUser,
    DBUserProject,
)

DB_NAME = "solar.db"


def get_user(username: str) -> DBUser | None:
    """Fetches a user by user_id from the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?;", (username,))
        user = cursor.fetchone()
    if user is None:
        return None
    return DBUser(*user)


def get_user_projects(user_id: str) -> list[DBUserProject]:
    """Fetches projects for a user by user_id from the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_projects WHERE user_id = ?;", (user_id,))
        user_projects = []
        for project in cursor.fetchall():
            row_id, *project = project
            user_projects.append(DBUserProject(*project))
    return user_projects


def get_all_projects() -> list[DBProject]:
    """Fetches all projects from the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT
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
                completed_date,
                is_completed
                  FROM projects;""")
        projects = cursor.fetchall()
    if projects is None:
        return []
    return [
        DBProject(
            project_id=project[0],
            name=project[1],
            location_city=project[2],
            location_country=project[3],
            latitude=project[4],
            longitude=project[5],
            bidding_zone=project[6],
            installed_capacity=project[7],
            description=project[8],
            number_of_cells=project[9],
            unit_price=project[10],
            completed_date=project[11],
            is_completed=project[12],
        )
        for project in projects
    ]


def get_project(project_id: str) -> DBProject | None:
    """Fetches a project by project_id from the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            (
                """SELECT 
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
                completed_date,
                is_completed
                FROM projects WHERE project_id = ?;
                """
            ),
            (project_id,),
        )
        project = cursor.fetchone()
    if project is None:
        return None
    return DBProject(
        project_id=project[0],
        name=project[1],
        location_city=project[2],
        location_country=project[3],
        latitude=project[4],
        longitude=project[5],
        bidding_zone=project[6],
        installed_capacity=project[7],
        description=project[8],
        number_of_cells=project[9],
        unit_price=project[10],
        completed_date=project[11],
        is_completed=project[12],
    )


def get_project_cells(panel_id: str) -> list[DBCell]:
    """Fetches cells for a panel by panel_id from the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cells WHERE panel_id = ?;", (panel_id,))
        cells = cursor.fetchall()
    if cells is None:
        return []
    return [DBCell(*cell) for cell in cells]


def get_project_panels(project_id: str) -> list[DBPanel]:
    """Fetches panels for a project by project_id from the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM panels WHERE project_id = ?;", (project_id,))
        panels = cursor.fetchall()
    if panels is None:
        return []
    return [DBPanel(*panel) for panel in panels]


def get_all_energy_data(project_id: str) -> list[DBEnergyDataPoint]:
    """Fetches energy data for a project by project_id from the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM energy_data WHERE project_id = ?;", (project_id,))
        energy_data = []
        for data_point in cursor.fetchall():
            row_id, *data_point = data_point
            energy_data.append(DBEnergyDataPoint(*data_point))

    return energy_data


def get_energy_data_range(project_id: str, start_date: str, end_date: str) -> list[DBEnergyDataPoint]:
    """Fetches energy data for a project by project_id and date range from the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM energy_data WHERE project_id = ? AND date BETWEEN ? AND ?;",
            (project_id, start_date, end_date),
        )
        energy_data = []
        for data_point in cursor.fetchall():
            row_id, *data_point = data_point
            energy_data.append(DBEnergyDataPoint(*data_point))
    return energy_data


def get_all_power_data(project_id: str) -> list[DBPowerDataPoint]:
    """Fetches power data for a project by project_id from the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM power_data WHERE project_id = ?;", (project_id,))
        power_data = []
        for data_point in cursor.fetchall():
            row_id, *data_point = data_point
            power_data.append(DBPowerDataPoint(*data_point))
    return power_data


def get_power_data_range(project_id: str, start_date: str, end_date: str) -> list[DBPowerDataPoint]:
    """Fetches power data for a project by project_id and date range from the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM power_data WHERE project_id = ? AND date BETWEEN ? AND ?;",
            (project_id, start_date, end_date),
        )
        power_data = []
        for data_point in cursor.fetchall():
            row_id, *data_point = data_point
            power_data.append(DBPowerDataPoint(*data_point))
    return power_data


if __name__ == "__main__":
    get_all_projects()
