import sqlite3
from functools import reduce
import operator


# https://stackoverflow.com/questions/595374/whats-the-function-like-sum-but-for-multiplication-product
def multiply_elements(iterable):
    return reduce(operator.mul, iterable, 1)


def create_database():
    connection = sqlite3.connect("solar.db")
    cursor = connection.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        is_active BOOLEAN DEFAULT 0,
        account_balance REAL,
        cells_owned INTEGER,
        projects_owned INTEGER,
        total_invested REAL,
        total_earnings REAL,
        total_energy_generated REAL,
        maximum_power_generation REAL
    );
    """)

    # Projects Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        location_city TEXT,
        location_country TEXT,
        latitude REAL,
        longitude REAL,
        bidding_zone TEXT NOT NULL,
        installed_capacity TEXT,
        description TEXT,
        plant_efficiency REAL,
        number_of_cells INTEGER,
        unit_price REAL,
        completed_date TEXT NULL,
        is_completed BOOLEAN DEFAULT 0
    );
    """)
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_projects_bidding_zone ON projects (bidding_zone);
    """)

    # User projects Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        project_id TEXT NOT NULL,
        percentage_owned REAL CHECK (percentage_owned BETWEEN 0 AND 100),
        time_of_purchase TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
    );
    """)

    # Panels Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS panels (
        id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
        description TEXT,
        cell_rows INTEGER,
        cell_columns INTEGER,
        FOREIGN KEY (project_id) REFERENCES projects(id)
    );
    """)

    # Cells Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cells (
        id TEXT PRIMARY KEY,
        user_id TEXT NULL,
        panel_id TEXT NOT NULL,
        price REAL,
        cell_index INTEGER,
        color TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
        FOREIGN KEY (panel_id) REFERENCES panels(id) ON DELETE CASCADE
    );
    """)

    # Energy Data Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS energy_data (
        id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        value REAL NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS power_data (
        id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        value REAL NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS energy_price (
        id TEXT PRIMARY KEY,
        bidding_zone TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        price REAL NOT NULL
    );
    """)
    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()
