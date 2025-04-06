import requests
import datetime
from backend.schemas import DBProject, DBEnergyPrice
from backend.db_interface import DBInterface
from backend.constants import DB_NAME

# Note: For prices might need to be extrapolated to get a 15m resolution

VALID_BIDDING_ZONES = [
    "AT",
    "BE",
    "CH",
    "CZ",
    "DE-LU",
    "DE-AT-LU",
    "DK1",
    "DK2",
    "FR",
    "HU",
    "IT-North",
    "NL",
    "NO2",
    "PL",
    "SE4",
    "SI",
]
db = DBInterface(db_name=DB_NAME)


def fetch_energy_price(bidding_zone: str, date: datetime.date) -> list[datetime.datetime, float]:
    """
    Fetches energy prices from the Energy Charts API for a specific bidding zone and date range.

    Returns:
        dict: A dictionary containing the energy prices data.
    """

    if bidding_zone not in VALID_BIDDING_ZONES:
        raise ValueError(f"Invalid bidding zone: {bidding_zone}. Valid zones are: {VALID_BIDDING_ZONES}")

    url = "https://api.energy-charts.info/price"

    start_time = datetime.datetime.combine(date, datetime.time(0, 0))
    end_time = datetime.datetime.combine(date, datetime.time(23, 0))

    time_format = "%Y-%m-%dT%H:%M:%SZ"
    params = {
        "bzn": bidding_zone,
        "start": start_time.strftime(time_format),
        "end": end_time.strftime(time_format),
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Error fetching data: {response.status_code} - {response.text}")

    data = response.json()

    unix_seconds = data["unix_seconds"]
    times = [datetime.datetime.fromtimestamp(ts) for ts in unix_seconds]
    price = data["price"]
    return list(zip(times, price, strict=True))


def store_energy_price(bidding_zone: str, date: datetime.date) -> None:
    """Stores energy prices in the database for a specific bidding zone and date range."""
    energy_prices = fetch_energy_price(bidding_zone, date)
    for timestamp, price in energy_prices:
        time_format = "%Y-%m-%dT%H:%M:%SZ"
        energy_price_data = DBEnergyPrice(
            bidding_zone=bidding_zone,
            timestamp=timestamp.strftime(time_format),
            price=price,
        )
        db.insert(energy_price_data)


def backfill_energy_price(from_date: datetime.date, to_date: datetime.date):
    """
    Backfills energy prices for all projects in the database from a start date to an end date.
    """
    dates = [from_date + datetime.timedelta(days=i) for i in range((to_date - from_date).days + 1)]
    projects = db.query(DBProject).all()
    for project in projects:
        for date in dates:
            store_energy_price(project.bidding_zone, date=date)
