import sqlite3
from schemas import DBTypes
from dataclasses import asdict
from typing import get_args, Any

DB_NAME = "solar.db"


def query_builder(table: str, data: DBTypes) -> tuple[str, tuple[Any, ...]]:
    """
    Constructs an SQL INSERT query and its corresponding values for a given table and data.

    Args:
        table (str): The name of the database table where the data will be inserted.
        data (DBTypes): The data to be inserted, formatted as compatible type defined by DBTypes.

    Returns:
        tuple[str, tuple[Any, ...]]: A tuple containing:
            - The SQL INSERT query as a string.
            - A tuple of values to be inserted into the table.

    Raises:
        TypeError: If the `data` argument is not an instance of a DBTypes subclass.
    """
    if not isinstance(data, get_args(DBTypes)):
        raise TypeError("Data must be a DBTypes subclass")

    data = asdict(data)
    query = f"""
            INSERT INTO {table} ({",".join(data.keys())})
            VALUES ({",".join(["?"] * len(data))});
        """
    return query, tuple(data.values())


def insert(tabel: str, data: DBTypes):
    """
    Inserts data into a specified table in the database.

    Args:
        tabel (str): The name of the table where the data will be inserted.
        data (DBTypes): The data to be inserted, formatted as compatible type defined by DBTypes.

    Raises:
        sqlite3.Error: If an error occurs during the database operation.

    Notes:
        - The function enables foreign key constraints before executing the query.
        - The `query_builder` function is used to construct the SQL query and
          corresponding values for insertion.
        - Changes are committed to the database after successful execution.
    """
    query, values = query_builder(tabel, data)

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute(query, values)
        conn.commit()


if __name__ == "__main__":
    from schemas import DBUser

    insert(
        "users",
        DBUser(
            id="user123",
            username="test_user",
            password="password123",
            account_balance=1000.0,
            cells_owned=5,
            projects_owned=2,
            total_invested=5000.0,
            total_earnings=200.0,
            total_energy_generated=1500.0,
            maximum_power_generation=300.0,
        ),
    )
