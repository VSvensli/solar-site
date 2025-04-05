import pytest
import os
import tempfile
import datetime
import sqlite3
from backend.db_interface import DBInterface, Query, DBInserter
from backend.schemas import DBPowerDataPoint, DBCell


@pytest.fixture
def temp_db():
    """Fixture to create a temporary SQLite database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_file:
        db_name = temp_file.name
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE power_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                value REAL NOT NULL
            );
            """
        )
        conn.commit()
        yield db_name
    finally:
        conn.close()
        os.remove(db_name)


@pytest.fixture
def db_interface(temp_db):
    """Fixture to provide a DBInterface instance."""
    return DBInterface(db_name=temp_db)


def test_insert_single_record(db_interface):
    """Test inserting a single record into the database."""
    data = DBPowerDataPoint(
        project_id="CSP_FR_001",
        timestamp="2025-02-21T10:00:00Z",
        value=123.45,
    )
    db_interface.insert(data)

    with sqlite3.connect(db_interface.db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM power_data;")
        result = cursor.fetchone()

    expected_result = (1, "CSP_FR_001", "2025-02-21T10:00:00Z", 123.45)
    assert result == expected_result


def test_insert_multiple_records(db_interface):
    """Test inserting multiple records into the database."""
    data = [
        DBPowerDataPoint(
            project_id="CSP_FR_001",
            timestamp="2025-02-21T10:00:00Z",
            value=123.45,
        ),
        DBPowerDataPoint(
            project_id="CSP_FR_002",
            timestamp="2025-02-21T11:00:00Z",
            value=678.90,
        ),
    ]
    db_interface.insert(data)

    with sqlite3.connect(db_interface.db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM power_data;")
        result = cursor.fetchall()

    expected_result = [
        (1, "CSP_FR_001", "2025-02-21T10:00:00Z", 123.45),
        (2, "CSP_FR_002", "2025-02-21T11:00:00Z", 678.90),
    ]
    assert len(result) == 2
    assert result[0] == expected_result[0]
    assert result[1] == expected_result[1]


def test_query_all_records(db_interface):
    """Test querying all records from the database."""
    data = [
        DBPowerDataPoint(
            project_id="CSP_FR_001",
            timestamp="2025-02-21T10:00:00Z",
            value=123.45,
        ),
        DBPowerDataPoint(
            project_id="CSP_FR_002",
            timestamp="2025-02-21T11:00:00Z",
            value=678.90,
        ),
    ]
    db_interface.insert(data)

    result = db_interface.query(DBPowerDataPoint).all()

    assert len(result) == 2
    assert result[0].project_id == "CSP_FR_001"
    assert result[1].project_id == "CSP_FR_002"


def test_query_with_filter(db_interface):
    """Test querying records with a filter."""
    data = [
        DBPowerDataPoint(
            project_id="CSP_FR_001",
            timestamp="2025-02-21T10:00:00Z",
            value=123.45,
        ),
        DBPowerDataPoint(
            project_id="CSP_FR_002",
            timestamp="2025-02-21T11:00:00Z",
            value=678.90,
        ),
    ]
    db_interface.insert(data)

    result = db_interface.query(DBPowerDataPoint).filter_by(project_id="CSP_FR_001").all()

    assert len(result) == 1
    assert result[0].project_id == "CSP_FR_001"


def test_query_select_specific_columns(db_interface):
    """Test selecting specific columns in a query."""
    data = [
        DBPowerDataPoint(
            project_id="CSP_FR_001",
            timestamp="2025-02-21T10:00:00Z",
            value=123.45,
        ),
        DBPowerDataPoint(
            project_id="CSP_FR_002",
            timestamp="2025-02-21T11:00:00Z",
            value=678.90,
        ),
    ]
    db_interface.insert(data)

    result = db_interface.query(DBPowerDataPoint).select("project_id", "value").all()

    expected_result = [
        ("CSP_FR_001", 123.45),
        ("CSP_FR_002", 678.90),
    ]
    assert len(result) == 2
    assert result[0] == expected_result[0]
    assert result[1] == expected_result[1]


def test_query_with_date_interval(db_interface):
    """Test querying records within a date interval."""
    data = [
        DBPowerDataPoint(
            project_id="CSP_FR_001",
            timestamp="2025-02-21T10:00:00Z",
            value=123.45,
        ),
        DBPowerDataPoint(
            project_id="CSP_FR_002",
            timestamp="2025-02-21T11:00:00Z",
            value=678.90,
        ),
    ]
    db_interface.insert(data)

    result = (
        db_interface.query(DBPowerDataPoint)
        .between(
            start_date=datetime.datetime(2025, 2, 21, 10),
            end_date=datetime.datetime(2025, 2, 21, 10, 30),
            time_column="timestamp",
        )
        .all()
    )

    assert len(result) == 1
    assert result[0].project_id == "CSP_FR_001"


def test_query_combined_filters(db_interface):
    """Test combining filters and date intervals in a query."""
    data = [
        DBPowerDataPoint(
            project_id="CSP_FR_001",
            timestamp="2025-02-21T10:00:00Z",
            value=123.45,
        ),
        DBPowerDataPoint(
            project_id="CSP_FR_002",
            timestamp="2025-02-21T11:00:00Z",
            value=678.90,
        ),
    ]
    db_interface.insert(data)

    result = (
        db_interface.query(DBPowerDataPoint)
        .filter_by(project_id="CSP_FR_001")
        .between(
            start_date=datetime.datetime(2025, 2, 21, 9),
            end_date=datetime.datetime(2025, 2, 21, 11),
            time_column="timestamp",
        )
        .all()
    )

    assert len(result) == 1
    assert result[0].project_id == "CSP_FR_001"
    assert result[0].timestamp == "2025-02-21T10:00:00Z"
    assert result[0].value == 123.45


def test_query_one_no_result(db_interface):
    """Test fetching a single result when no records match."""
    result = db_interface.query(DBPowerDataPoint).filter_by(project_id="NON_EXISTENT").one()

    assert result is None


def test_query_all_no_result(db_interface):
    """Test fetching a multiple result when no records match."""
    result = db_interface.query(DBPowerDataPoint).filter_by(project_id="NON_EXISTENT").all()

    assert result == []


def test_verify_inputs_valid_data():
    """Test _verify_inputs with valid data."""
    inserter = DBInserter("test_db")
    data = [
        DBPowerDataPoint(
            project_id="CSP_FR_001",
            timestamp="2025-02-21T10:00:00Z",
            value=123.45,
        ),
        DBPowerDataPoint(
            project_id="CSP_FR_001",
            timestamp="2025-02-21T11:00:00Z",
            value=678.90,
        ),
    ]
    try:
        inserter._verify_inputs(data)
    except Exception as e:
        pytest.fail(f"Unexpected exception raised: {e}")


def test_verify_inputs_empty_list():
    """Test _verify_inputs with an empty list."""
    inserter = DBInserter("")
    data = []
    with pytest.raises(ValueError, match="The list is empty"):
        inserter._verify_inputs(data)


def test_verify_inputs_mixed_types():
    """Test _verify_inputs with mixed types in the list."""
    inserter = DBInserter("")
    data = [
        DBPowerDataPoint(
            project_id="CSP_FR_001",
            timestamp="2025-02-21T10:00:00Z",
            value=123.45,
        ),
        "invalid_data",
    ]
    with pytest.raises(TypeError, match="All items in the list must be a DBTypes subclass"):
        inserter._verify_inputs(data)


def test_verify_inputs_different_table_types():
    """Test _verify_inputs with different table types."""
    inserter = DBInserter("")

    data = [
        DBPowerDataPoint(
            project_id="CSP_FR_001",
            timestamp="2025-02-21T10:00:00Z",
            value=123.45,
        ),
        DBCell(
            id="cell_001",
            user_id=None,
            panel_id="panel_001",
            price=100.0,
            cell_index=1,
            color="red",
        ),
    ]
    with pytest.raises(TypeError, match="All items in the list must be of the same type"):
        inserter._verify_inputs(data)


def test_verify_input_valid_data():
    """Test _verify_input with valid data."""
    inserter = DBInserter("")
    data = DBPowerDataPoint(
        project_id="CSP_FR_001",
        timestamp="2025-02-21T10:00:00Z",
        value=123.45,
    )
    try:
        inserter._verify_input(data)
    except Exception as e:
        pytest.fail(f"Unexpected exception raised: {e}")


def test_verify_input_invalid_data():
    """Test _verify_input with invalid data."""
    inserter = DBInserter("")
    data = "invalid_data"
    with pytest.raises(TypeError, match="Data must be a DBTypes subclass"):
        inserter._verify_input(data)


def test_interter_query_builder():
    """Test _query_builder generates correct SQL query."""
    inserter = DBInserter("")
    data = DBPowerDataPoint(
        project_id="CSP_FR_001",
        timestamp="2025-02-21T10:00:00Z",
        value=123.45,
    )
    query = inserter._query_builder(data)
    expected_query = """
                INSERT INTO power_data (id,project_id,timestamp,value)
                VALUES (?,?,?,?);
                """
    assert query.strip() == expected_query.strip()


def test_query_filter_by_invalid_field():
    """Test filtering by a field that does not exist in the model."""
    query = Query(DBPowerDataPoint, "")
    with pytest.raises(AttributeError, match="DBPowerDataPoint has no field invalid_field"):
        query.filter_by(invalid_field="value")


def test_query_select_no_columns():
    """Test selecting no columns explicitly."""
    query = Query(DBPowerDataPoint, "")
    with pytest.raises(ValueError, match="At least one column must be specified"):
        query.select()


def test_query_between_invalid_column():
    """Test filtering by a date interval with an invalid column."""
    query = Query(DBPowerDataPoint, "")
    with pytest.raises(AttributeError, match="DBPowerDataPoint has no field invalid_column"):
        query.between(
            start_date=datetime.datetime(2025, 2, 21, 10),
            end_date=datetime.datetime(2025, 2, 21, 11),
            time_column="invalid_column",
        )


def test_query_between_invalid_date_order():
    """Test filtering by a date interval where start_date is after end_date."""
    query = Query(DBPowerDataPoint, "")
    with pytest.raises(ValueError, match="Start date must be before end date"):
        query.between(
            start_date=datetime.datetime(2025, 2, 21, 11),
            end_date=datetime.datetime(2025, 2, 21, 10),
            time_column="timestamp",
        )
