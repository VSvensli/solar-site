import sqlite3
import datetime
from dataclasses import fields
from collections import namedtuple
from schemas import (
    DBProject,
    DBPanel,
    DBCell,
    DBEnergyDataPoint,
    DBPowerDataPoint,
    DBUser,
    DBUserProject,
    DBTypes,
)

DB_NAME = "solar.db"
IntervalSelection = namedtuple("IntervalSelection", ["column", "start_date", "end_date"])


class SimpleORM:
    def __init__(self, db_name: str = DB_NAME):
        self.db_name = db_name

    @classmethod
    def quary(cls, model_class: DBTypes) -> "Query":
        return Query(model_class, cls().db_name)


class Query:
    def __init__(self, model_class: DBTypes, db_name: str = ""):
        self.model_class = model_class
        self.selection = "*"
        self.filters = {}
        self.interval = None
        self.db_name = db_name

    def _build_query(self):
        """Build the SQL query based on the filters."""
        query = f"SELECT {self.selection} FROM {self.model_class.__table_name__} "
        if self.filters:
            query += "WHERE "
        conditions = []
        params = []
        for key, value in self.filters.items():
            conditions.append(f"{key} = ?")
            params.append(value)
        if self.interval:
            conditions.append(f"{self.interval.column} BETWEEN ? AND ?")
            params.extend([self.interval.start_date, self.interval.end_date])
        query += " AND ".join(conditions) + ";"
        return query, tuple(params)

    def filter_by(self, **kwargs):
        """Filter the query based on the provided keyword arguments."""
        for key, value in kwargs.items():
            if key in [f.name for f in fields(self.model_class)]:
                self.filters[key] = value
            else:
                raise AttributeError(f"{self.model_class.__name__} has no field {key}")
        return self

    def between(self, start_date: datetime.datetime, end_date: datetime.datetime, time_column: str = "date"):
        """Filter the query to include only records between the specified dates."""
        if time_column not in [f.name for f in fields(self.model_class)]:
            raise AttributeError(f"{self.model_class.__name__} has no field {time_column}")

        str_format = "%Y-%m-%dT%H:%M:%SZ"
        start_date = start_date.strftime(str_format)
        end_date = end_date.strftime(str_format)
        if start_date > end_date:
            raise ValueError("Start date must be before end date")

        self.interval = IntervalSelection(time_column, start_date, end_date)
        return self

    def select(self, *args):
        """Select specific columns from the query."""
        self.selection = ", ".join(args)
        return self

    def all(self) -> list[DBTypes]:
        """Fetch all results from the query."""
        query, params = self._build_query()
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
        result = cursor.fetchall()
        return [self.model_class(*row) for row in result]

    def one(self) -> DBTypes | None:
        query, params = self._build_query()
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
        result = cursor.fetchone()
        return self.model_class(*result)


def get_user(username: str) -> DBUser | None:
    """Fetches a user by username from the database."""
    with SimpleORM(DB_NAME) as orm:
        quary = "SELECT * FROM users WHERE username = ?;"
        user = orm.fetch_one(query=quary, params=(username,), return_type=DBUser)
    return user


def get_user_projects(user_id: str) -> list[DBUserProject]:
    """Fetches projects for a user by user_id from the database."""
    with SimpleORM(DB_NAME) as orm:
        query = "SELECT * FROM user_projects WHERE user_id = ?;"
        user_projects = orm.fetch_all(query=query, params=(user_id,), return_type=DBUserProject)
    return user_projects


def get_all_projects() -> list[DBProject]:
    """Fetches all projects from the database."""
    with SimpleORM(DB_NAME) as orm:
        query = "SELECT * FROM projects;"
        projects = orm.fetch_all(query=query, return_type=DBProject)
    return projects


def get_project(project_id: str) -> DBProject | None:
    """Fetches a project by project_id from the database."""
    with SimpleORM(DB_NAME) as orm:
        query = "SELECT * FROM projects WHERE id = ?;"
        project = orm.fetch_one(query=query, params=(project_id,), return_type=DBProject)
    return project


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
    import pprint

    orm = SimpleORM()
    pprint.pprint(
        orm.quary(DBPowerDataPoint)
        .filter_by(project_id="CSP_FR_001")
        .between(
            start_date=datetime.datetime(2025, 2, 21, 10),
            end_date=datetime.datetime(2025, 2, 21, 11),
            time_column="timestamp",
        )
        .all()
    )
