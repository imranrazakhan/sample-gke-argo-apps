from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .base import Base


class WeatherOrigin(Enum):
    """
    Enumeration representing the origin of weather data from different providers.

    Attributes:
        METEOMATICS: Weather data from Meteomatics.
        ERA5: Weather data from ERA5.
    """

    METEOMATICS = "meteomatics"
    ERA5 = "ERA5"


class WeatherData(Base):
    """
    Table representing weather time series data.

    Attributes:
        timestamp (datetime): Timestamp of the weather data.
        temperature_2m (float): Temperature at 2 meters.
        relative_humidity_2m (float): Relative humidity at 2 meters.
        dew_point_2m (float): Dew point at 2 meters.
        msl_pressure (float): Mean sea level pressure.
        sfc_pressure (float): Surface pressure.
        low_cloud_cover (float): Low cloud cover percentage.
        effective_cloud_cover (float): Effective cloud cover percentage.
        total_cloud_cover (float): Total cloud cover percentage.
        ceiling_height_agl (float): Ceiling height above ground level.
        precipitation (float): Precipitation
        wind_dir_10m (float): Wind direction at 10 meters.
        wind_speed_u_10m (float): Wind speed u-component at 10 meters.
        wind_speed_v_10m (float): Wind speed v-component at 10 meters.
        wind_dir_100m (float): Wind direction at 100 meters.
        wind_speed_u_100m (float): Wind speed u-component at 100 meters.
        wind_speed_v_100m (float): Wind speed v-component at 100 meters.
        snow_depth (float): Snow depth.
        clear_sky_rad (float): Clear sky radiation
        diffuse_rad (float): Diffuse radiation
        direct_rad (float): Direct radiation
        global_rad (float): Global radiation
        meta_id (int): Foreign key referencing WeatherMeta table.

       meta (WeatherMeta): Relationship to WeatherMeta table.

    Methods:
        __repr__(): Represent the WeatherData object as a string.
    """

    __tablename__ = "weather_data"

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )
    temperature_2m: Mapped[float] = mapped_column(nullable=True)
    relative_humidity_2m: Mapped[float] = mapped_column(nullable=True)
    dew_point_2m: Mapped[float] = mapped_column(nullable=True)
    msl_pressure: Mapped[float] = mapped_column(nullable=True)
    sfc_pressure: Mapped[float] = mapped_column(nullable=True)
    low_cloud_cover: Mapped[float] = mapped_column(nullable=True)
    effective_cloud_cover: Mapped[float] = mapped_column(nullable=True)
    total_cloud_cover: Mapped[float] = mapped_column(nullable=True)
    ceiling_height: Mapped[float] = mapped_column(nullable=True)
    precipitation: Mapped[float] = mapped_column(nullable=True)
    wind_dir_10m: Mapped[float] = mapped_column(nullable=True)
    wind_speed_u_10m: Mapped[float] = mapped_column(nullable=True)
    wind_speed_v_10m: Mapped[float] = mapped_column(nullable=True)
    wind_dir_100m: Mapped[float] = mapped_column(nullable=True)
    wind_speed_u_100m: Mapped[float] = mapped_column(nullable=True)
    wind_speed_v_100m: Mapped[float] = mapped_column(nullable=True)
    snow_depth: Mapped[float] = mapped_column(nullable=True)
    clear_sky_rad: Mapped[float] = mapped_column(nullable=True)
    diffuse_rad: Mapped[float] = mapped_column(nullable=True)
    direct_rad: Mapped[float] = mapped_column(nullable=True)
    global_rad: Mapped[float] = mapped_column(nullable=True)

    meta_id: Mapped[int] = mapped_column(
        ForeignKey("weather_meta.id"), primary_key=True
    )

    meta: Mapped["WeatherMeta"] = relationship(back_populates="data")

    def __repr__(self) -> str:
        return f"<WeatherData timestamp={self.timestamp}, meta_id={self.meta_id}>"


class WeatherMeta(Base):
    """
    Table representing metadata for weather data.

    Attributes:
        id (int): Primary key.
        origin (WeatherOrigin): Origin of weather data.
        latitude (float): latitude coordinate
        longitude (float): longitude coordinate
        comment (str): description of weather data and more insides
        data (WeatherData): Relationship to WeatherData table.

    Methods:
        __repr__(): Represent the WeatherMeta object as a string.
    """

    __tablename__ = "weather_meta"
    __table_args__ = (UniqueConstraint("origin", "latitude", "longitude"),)

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    origin: Mapped[WeatherOrigin] = mapped_column(nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    comment: Mapped[str] = mapped_column(nullable=True)

    data: Mapped["WeatherData"] = relationship(back_populates="meta")

    def __repr__(self) -> str:
        return (
            f"<WeatherMeta longitude={self.longitude}, latitude={self.latitude}, "
            f"origin={self.origin}"
        )
