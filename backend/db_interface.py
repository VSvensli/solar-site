import sqlite3
import datetime
from dataclasses import fields, asdict, astuple
from typing import get_args


from backend.constants import DB_NAME
from collections import namedtuple
from backend.schemas import DBTypes


IntervalSelection = namedtuple("IntervalSelection", ["column", "start_date", "end_date"])


class DBInterface:
    def __init__(self, db_name: str):
        self.db_name = db_name

    def quary(self, model_class: DBTypes) -> "Query":
        return Query(model_class, self.db_name)

    def insert(self, data: DBTypes) -> None:
        inserter = DBInserter(self.db_name)
        inserter.insert(data)


class DBInserter:
    def __init__(self, db_name):
        self.db_name = db_name

    def _verify_inputs(self, data: list[DBTypes]) -> None:
        if not data:
            raise ValueError("The list is empty")
        if not all(isinstance(d, get_args(DBTypes)) for d in data):
            raise TypeError("All items in the list must be a DBTypes subclass")
        if not len(set([type(d) for d in data])) == 1:
            raise TypeError("All items in the list must be of the same type")
        if not all(hasattr(d, "__table_name__") for d in data):
            raise TypeError("All items in the list must be of the same table type")

    def _verify_input(self, data: DBTypes) -> None:
        if not isinstance(data, get_args(DBTypes)):
            raise TypeError("Data must be a DBTypes subclass")

    @staticmethod
    def _query_builder(data: DBTypes) -> str:
        """Constructs an SQL INSERT query and its corresponding values for a given table and data.

        Args:
            table (str): The name of the database table where the data will be inserted.
            data (DBTypes): The data to be inserted, formatted as compatible type defined by DBTypes.

        Returns:
            tuple[str, tuple[Any, ...]]: A tuple containing:
                - The SQL INSERT query as a string.
                - A tuple of values to be inserted into the table.

        Raises:
            TypeError: If the `data` argument is not an instance of a DBTypes subclass."""
        table_name = data.__table_name__
        data = asdict(data)
        query = f"""
                INSERT INTO {table_name} ({",".join(data.keys())})
                VALUES ({",".join(["?"] * len(data))});
                """
        return query

    def insert(self, data: DBTypes | list[DBTypes]):
        """Inserts data into a specified table in the database.

        Args:
            tabel (str): The name of the table where the data will be inserted.
            data (DBTypes): The data to be inserted, formatted as compatible type defined by DBTypes.

        Raises:
            sqlite3.Error: If an error occurs during the database operation.

        Notes:
            Enables foreign key constraints before executing the query(PRAGMA foreign_keys = ON;)."""
        insert_multiple = isinstance(data, list)

        if insert_multiple:
            self._verify_inputs(data)
            query = self._query_builder(data[0])
            values = [astuple(d) for d in data]
        else:
            self._verify_input(data)
            query = self._query_builder(data)
            values = astuple(data)

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            if insert_multiple:
                cursor.executemany(query, values)
            else:
                cursor.execute(query, values)

            conn.commit()


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


if __name__ == "__main__":
    import pprint
    from backend.schemas import DBPowerDataPoint

    db = DBInterface(db_name=DB_NAME)
    data = (
        db.quary(DBPowerDataPoint)
        .filter_by(project_id="CSP_FR_001")
        .between(
            start_date=datetime.datetime(2025, 2, 21, 10),
            end_date=datetime.datetime(2025, 2, 21, 11),
            time_column="timestamp",
        )
        .all()
    )

    pprint.pprint(data)
