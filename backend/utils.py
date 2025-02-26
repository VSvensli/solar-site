import sqlite3


def create_database():
    connection = sqlite3.connect("solar.db")
    cursor = connection.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
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
        project_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        location_city TEXT,
        location_country TEXT,
        latitude REAL,
        longitude REAL,
        bidding_zone TEXT,
        installed_capacity TEXT,
        description TEXT,
        number_of_cells INTEGER,
        unit_price REAL,
        is_completed BOOLEAN DEFAULT 0,
        completed_date TEXT NULL,
        FOREIGN KEY (bidding_zone) REFERENCES energy_price(bidding_zone) ON DELETE CASCADE
    );
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
        FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
    );
    """)

    # Panels Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS panels (
        panel_id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
        description TEXT,
        cell_rows INTEGER,
        cell_columns INTEGER,
        FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
    );
    """)

    # Cells Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cells (
        cell_id TEXT PRIMARY KEY,
        owner_id TEXT NULL,
        panel_id TEXT NOT NULL,
        price REAL,
        cell_index INTEGER,
        color TEXT,
        FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE SET NULL,
        FOREIGN KEY (panel_id) REFERENCES Panels(panel_id) ON DELETE CASCADE
    );
    """)

    # Energy Metrics Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS energy_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        value REAL NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS power_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        value REAL NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS energy_price (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bidding_zone TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        price REAL NOT NULL,
        FOREIGN KEY (bidding_zone) REFERENCES projects(bidding_zone) ON DELETE CASCADE
    );
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()
