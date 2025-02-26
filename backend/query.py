import sqlite3

DB_NAME = "solar.db"


def get_all_projects():
    """Fetches all projects from the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects;")
        projects = cursor.fetchall()
    return projects


def get_project(project_id: str):
    """Fetches a project by project_id from the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE project_id = ?;", (project_id,))
        project = cursor.fetchone()
    return project


def get_project_panels(project_id: str):
    """Fetches panels for a project by project_id from the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM panels WHERE project_id = ?;", (project_id,))
        panels = cursor.fetchall()
    return panels


def get_project_cells(panel_id: str):
    """Fetches cells for a panel by panel_id from the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cells WHERE panel_id = ?;", (panel_id,))
        cells = cursor.fetchall()
    return cells


def get_all_energy_data(project_id: str):
    """Fetches energy data for a project by project_id from the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM energy_data WHERE project_id = ?;", (project_id,))
        energy_data = cursor.fetchall()
    return energy_data


def get_energy_data_range(project_id: str, start_date: str, end_date: str):
    """Fetches energy data for a project by project_id and date range from the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM energy_data WHERE project_id = ? AND date BETWEEN ? AND ?;",
            (project_id, start_date, end_date),
        )
        energy_data = cursor.fetchall()
    return energy_data


def get_all_power_data(project_id: str):
    """Fetches power data for a project by project_id from the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM power_data WHERE project_id = ?;", (project_id,))
        power_data = cursor.fetchall()
    return power_data


def get_power_data_range(project_id: str, start_date: str, end_date: str):
    """Fetches power data for a project by project_id and date range from the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM power_data WHERE project_id = ? AND date BETWEEN ? AND ?;",
            (project_id, start_date, end_date),
        )
        power_data = cursor.fetchall()
    return power_data
