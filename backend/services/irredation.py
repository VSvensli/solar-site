from dataclasses import dataclass
import math
import random
from datetime import datetime, timedelta
from typing import Literal
import uuid

from backend.schemas import DBPowerDataPoint, DBProject, DBEnergyDataPoint
from backend.db_interface import DBInterface
from backend.constants import DB_NAME


@dataclass
class OpenWeatherIrradianceRequest:
    lat: float
    lon: float
    date: str
    interval: str
    api_key: str


@dataclass
class IrradianceInterval:
    start: str
    end: str
    clear_sky_ghi: float
    clear_sky_dni: float
    clear_sky_dhi: float
    cloudy_sky_ghi: float
    cloudy_sky_dni: float
    cloudy_sky_dhi: float


@dataclass
class DailyIrradiance:
    clear_sky_ghi: float
    clear_sky_dni: float
    clear_sky_dhi: float
    cloudy_sky_ghi: float
    cloudy_sky_dni: float
    cloudy_sky_dhi: float


@dataclass
class OpenWeatherIrradianceResponse:
    lat: float
    lon: float
    date: str
    interval: str
    tz: str
    sunrise: str
    sunset: str
    daily: list[DailyIrradiance]
    intervals: list[IrradianceInterval]


def solar_irradiance_profile(
    latitude_deg: float, date: datetime, interval_str: Literal["15m", "1h"] = "15m", noise_level: float = 0.2
) -> list:
    """
    Estimates solar irradiance (in W/m²) throughout a day with weather-like noise.

    Parameters:
        latitude_deg (float): Latitude in degrees (-90 to 90). North is positive.
        date (datetime): Date to calculate solar irradiance.
        interval_minutes (int): Time resolution in minutes.
        noise_level (float): Cloudiness/variability factor (0.0 = clear sky).

    Returns:
        list of tuples: (datetime, irradiance in W/m²)
    """
    if interval_str == "15m":
        interval_minutes = 15
    elif interval_str == "1h":
        interval_minutes = 60
    else:
        raise ValueError("Interval must be '15m' or '1h'")

    latitude = math.radians(latitude_deg)
    day_of_year = date.timetuple().tm_yday

    # Solar declination angle (radians)
    declination = math.radians(23.44) * math.sin(math.radians(360 * (day_of_year - 81) / 365))

    # Estimate day length
    cos_omega = -math.tan(latitude) * math.tan(declination)
    cos_omega = max(-1.0, min(1.0, cos_omega))
    omega = math.acos(cos_omega)
    day_length = (2 * omega * 180 / math.pi) / 15  # hours

    # Solar noon setup
    half_day = timedelta(hours=day_length / 2)
    solar_noon = datetime(date.year, date.month, date.day, 12, 0)
    sunrise = solar_noon - half_day
    sunset = solar_noon + half_day

    # Earth-Sun distance factor (eccentricity correction)
    d = 1 + 0.033 * math.cos(math.radians(360 * day_of_year / 365))

    # Solar constant at top of atmosphere
    S0 = 1361  # W/m²

    # Generate time series
    current_time = datetime(date.year, date.month, date.day, 0, 0)
    interval = timedelta(minutes=interval_minutes)

    profile = []

    dayly_irradiance = 0.0
    for _ in range(int(24 * 60 / interval_minutes)):
        # Time from solar noon in hours
        time_diff = (current_time - solar_noon).total_seconds() / 3600.0
        hour_angle = math.radians(15 * time_diff)

        # Solar elevation angle
        sin_elevation = math.sin(latitude) * math.sin(declination) + math.cos(latitude) * math.cos(
            declination
        ) * math.cos(hour_angle)

        if sin_elevation > 0:
            # Air mass approximation (simplified, avoids divide-by-zero)
            air_mass = 1 / max(0.1, sin_elevation)

            # Clear-sky irradiance estimate (simplified model)
            irradiance = S0 * d * sin_elevation * math.exp(-0.14 * air_mass)

            # Weather noise
            noise = random.gauss(mu=1.0, sigma=noise_level)
            irradiance *= max(0.0, noise)
        else:
            irradiance = 0.0

        profile.append((current_time, irradiance))
        current_time += interval
        dayly_irradiance += irradiance * interval_minutes / 60.0  # Convert to Wh/m²

    return profile, sunrise, sunset, dayly_irradiance


def fake_openweather_irradiance_api(request: OpenWeatherIrradianceRequest) -> OpenWeatherIrradianceResponse:
    iradiance_data, sunrise, sunset, daily_irradiance = solar_irradiance_profile(
        latitude_deg=request.lat,
        date=datetime.strptime(request.date, "%Y-%m-%d"),
        interval_str=request.interval,
        noise_level=0.2,
    )
    daily_irradiance = DailyIrradiance(
        clear_sky_ghi=0,
        clear_sky_dni=0,
        clear_sky_dhi=0,
        cloudy_sky_ghi=daily_irradiance,
        cloudy_sky_dni=0,
        cloudy_sky_dhi=0,
    )
    intervals = [
        IrradianceInterval(
            start=interval[0].strftime("%Y-%m-%dT%H:%M:%SZ"),
            end=(interval[0] + timedelta(minutes=int(request.interval[:-1]))).strftime("%Y-%m-%dT%H:%M:%SZ"),
            clear_sky_ghi=0,
            clear_sky_dni=0,
            clear_sky_dhi=0,
            cloudy_sky_ghi=interval[1],
            cloudy_sky_dni=0,
            cloudy_sky_dhi=0,
        )
        for interval in iradiance_data
    ]
    return OpenWeatherIrradianceResponse(
        lat=request.lat,
        lon=request.lon,
        date=request.date,
        interval=request.interval,
        tz="UTC",
        sunrise=sunrise.strftime("%Y-%m-%dT%H:%M:%SZ"),
        sunset=sunset.strftime("%Y-%m-%dT%H:%M:%SZ"),
        daily=[daily_irradiance],
        intervals=intervals,
    )


def store_irridation_data(time: datetime = datetime.now()):
    # This function should be implemented to store irradiance data
    db = DBInterface(db_name=DB_NAME)
    projects = db.query(DBProject).all()

    for project in projects:
        request = OpenWeatherIrradianceRequest(
            lat=project.latitude,
            lon=project.longitude,
            date=time.strftime("%Y-%m-%d"),
            interval="15m",
            api_key="fake_api_key",
        )
        response = fake_openweather_irradiance_api(request)
        for interval in response.intervals:
            data_point = DBPowerDataPoint(
                id=uuid.uuid4().hex,
                project_id=project.id,
                timestamp=interval.start,
                value=interval.cloudy_sky_ghi * project.plant_efficiency,
            )
            db.insert(data_point)

        energy = DBEnergyDataPoint(
            id=uuid.uuid4().hex,
            project_id=project.id,
            timestamp=response.intervals[0].start,
            value=response.daily[0].cloudy_sky_ghi * project.plant_efficiency,
        )
        db.insert(energy)


def backfill_irridation_data(from_date: datetime, to_date: datetime):
    dates = [from_date + timedelta(days=i) for i in range((to_date - from_date).days + 1)]
    for date in dates:
        store_irridation_data(date)
