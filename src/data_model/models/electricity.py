from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from datetime import datetime
from .base import Base


class ElectricityPrice(Base):
    """
    Table containing electricity prices.

    Attributes:
        timestamp (datetime): Timestamp of the electricity price.
        price (float): The actual price
        price_type_id (int): Link to the electricity metaobject.
        price_period_id (int): Link to the electricity period metaobject.
    Methods:
        __repr__(): Represent the Offer object as a string.
    """

    __tablename__ = "electricity_price"

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        primary_key=True,
    )
    price: Mapped[float] = mapped_column(nullable=False)
    price_type_id: Mapped[int] = mapped_column(
        ForeignKey("electricity_price_type.id"),
        primary_key=True,
    )
    price_period_id: Mapped[int] = mapped_column(
        ForeignKey("electricity_price_period.id"),
        primary_key=True,
    )

    price_type: Mapped["ElectricityPriceType"] = relationship(
        back_populates="electricity_price_data"
    )
    price_period: Mapped["ElectricityPricePeriod"] = relationship(
        back_populates="electricity_price_data"
    )

    def __repr__(self) -> str:
        return f"<ElectricityPrice timestamp={self.timestamp}, price={self.price}>"


class ElectricityPriceType(Base):
    """
    Table containing information about electricity price types and sources.

    Attributes:
        id (int): Primary key.
        price_type (str): Type of the electricity price.
        source (str): Source of the electricity price.
    Methods:
        __repr__(): Represent the ElectricityPriceType object as a string.
    """

    __tablename__ = "electricity_price_type"

    id: Mapped[int] = mapped_column(
        autoincrement=True,
        primary_key=True,
    )
    price_type: Mapped[str] = mapped_column(
        nullable=False,
    )
    source: Mapped[str] = mapped_column(
        nullable=False,
    )

    electricity_price_data: Mapped["ElectricityPrice"] = relationship(
        back_populates="price_type"
    )
    intraday_continuous_data: Mapped["IntradayContinuousPrice"] = relationship(
        back_populates="price_type"
    )

    def __repr__(self) -> str:
        return (
            f"ElectricityPriceType id={self.id}, price_type={self.price_type}, "
            f"source={self.source}>"
        )


class ElectricityPricePeriod(Base):
    """
    Table containing additional meta information about electricity prices.
    Connected to ElectricityPriceType.

    Attributes:
        id (int): Primary key.
        price_type_id (int): Foreign key to the electricity price meta table.
        min_datetime (datetime): Earliest entry in electricity prices.
        max_datetime (datetime): Latest entry in electricity prices.
        upload_timestamp (datetime): Date and time of the data upload.
        inflation (bool): Flag indicating if the data is inflation adjusted.
    Methods:
        __repr__(): Represent the ElectricityPricePeriod object as a string.
    """

    __tablename__ = "electricity_price_period"

    id: Mapped[int] = mapped_column(
        autoincrement=True,
        primary_key=True,
    )
    price_type_id: Mapped[int] = mapped_column(ForeignKey("electricity_price_type.id"))
    min_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    max_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    upload_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    inflation: Mapped[bool] = mapped_column(
        nullable=False,
    )

    electricity_price_data: Mapped["ElectricityPrice"] = relationship(
        back_populates="price_period"
    )
    intraday_continuous_data: Mapped["IntradayContinuousPrice"] = relationship(
        back_populates="price_period"
    )

    def __repr__(self) -> str:
        return (
            f"<ElectricityPricePeriod id={self.id}, meta_id={self.price_type_id}, "
            f"upload_timestamp={self.upload_timestamp}>"
        )


class IntradayContinuousPrice(Base):
    """
    Table containing intraday continuous prices in EUR and MWh.

    Attributes:
        price_type_id (int): Foreign key to the electricity price meta table.
        price_period_id (int): Foreign key to the electricity price period meta
            table.
        trade_id (float): The tradeId is the identifier of the trade.
        remote_trade_id (float): The remote tradeId is the identifier of the trade
            if executed on the SOB.
        side (Boolean): 0 = buy, 1 = sell, identifies the side the trade leg.
        product (str): The product type identifies the product the trade was
            created on (XBID, Intraday, Hour, Half Hour, Quarter Hour).
        delivery_start (datetime): Delivery start of the contract.
        delivery_end (datetime): Delivery end of the contract.
        execution_time (datetime): Trading time of the contract.
        delivery_area (str): Delivery area where the trade leg is located
            (DE1: DE-ENBW, DE2: DE-AMP, DE3: DE-TPS, DE4: DE-50HZ)
        trade_phase (str): Phase the contract of the trade at the time of matching
            (CONT, SDAT or AUCT).
        user_defined_block (str): Indicates if the trade is on a user-defined
            block contract or not.
        self_trade (str): Indicates if the trade is a self-trade or if it is not
            possible to be.
        price (float): The price of the trade in EUR.
        volume (float): The volume of the trade in MWh.
        order_id (float): Reference to the order the trade leg is related to.

    Methods:
        __repr__(): Represent the IntradayContinuousPrice object as a string.
    """

    __tablename__ = "intraday_continuous_price"

    price_type_id: Mapped[int] = mapped_column(
        ForeignKey("electricity_price_type.id"),
        primary_key=True,
    )
    price_period_id: Mapped[int] = mapped_column(
        ForeignKey("electricity_price_period.id"),
        primary_key=True,
    )
    trade_id: Mapped[float] = mapped_column(
        nullable=False,
    )
    remote_trade_id: Mapped[float] = mapped_column(
        nullable=False,
    )
    side: Mapped[bool] = mapped_column(
        nullable=False,
    )
    product: Mapped[str] = mapped_column(
        nullable=False,
    )
    delivery_start: Mapped[datetime] = mapped_column(
        DateTime(
            timezone=True,
        ),
        nullable=False,
    )
    delivery_end: Mapped[datetime] = mapped_column(
        DateTime(
            timezone=True,
        ),
        nullable=False,
    )
    execution_time: Mapped[datetime] = mapped_column(
        DateTime(
            timezone=True,
        ),
        nullable=False,
    )
    delivery_area: Mapped[str] = mapped_column(
        nullable=False,
    )
    trade_phase: Mapped[str] = mapped_column(
        nullable=False,
    )
    user_defined_block: Mapped[str] = mapped_column(
        nullable=False,
    )
    self_trade: Mapped[str] = mapped_column(
        nullable=False,
    )
    price: Mapped[float] = mapped_column(nullable=False)
    volume: Mapped[float] = mapped_column(
        nullable=False,
    )
    order_id: Mapped[float] = mapped_column(
        nullable=False,
    )
    UniqueConstraint(
        delivery_start,
        delivery_end,
        execution_time,
        delivery_area,
    )

    price_type: Mapped["ElectricityPriceType"] = relationship(
        back_populates="intraday_continuous_data"
    )
    price_period: Mapped["ElectricityPricePeriod"] = relationship(
        back_populates="intraday_continuous_data"
    )

    def __repr__(self) -> str:
        return (
            f"<IntradayContinuousPrice product={self.product}, price={self.price}, "
            f"volume={self.volume},>"
        )


class Netztransparenz(Base):
    """
    Table storing net transparency data.

    Attributes:
        id (int): Primary key.
        timestamp (str): Date and time of the data.
        base_load_price (float): MW-EPEX in Euros/MWh.
        capture_price_wind_onshore (float): MW Wind Onshore in Euros/MWh.
        capture_price_wind_onshore_remote (float): PM Wind Onshore fernsteuerbar
            in Euros/MWh.
        capture_price_wind_offshore (float): MW Wind Offshore in ct/MWh.
        capture_price_wind_offshore_remote (float): PM Wind Offshore fernsteuerbar
            in Euros/MWh.
        capture_price_solar(float): MW Solar in Euros/MWh.
        capture_price_solar_remote (float): PM Solar fernsteuerbar in Euros/MWh.
        mw_steuerbar_euro_per_mwh (float): MW steuerbar in Euros/MWh.
        pm_steuerbar_euro_per_mwh (float): PM steuerbar in Euros/MWh.
        negative_hours_6h (int): Negative Stunden (6H).
        negative_hours_4h (int): Negative Stunden (4H).
        negative_hours_3h (int): Negative Stunden (3H).
        negative_hours_1h (int): Negative Stunden (1H).
        year (int): Year.
        month (int): Month.
    """

    __tablename__ = "netztransparenz"

    __table_args__ = (UniqueConstraint("year", "month"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int] = mapped_column(nullable=False)
    month: Mapped[int] = mapped_column(nullable=False)

    base_load_price: Mapped[float] = mapped_column(nullable=False)
    capture_price_wind_onshore: Mapped[float] = mapped_column(nullable=False)
    capture_price_wind_onshore_remote: Mapped[float] = mapped_column(nullable=True)
    capture_price_wind_offshore: Mapped[float] = mapped_column(nullable=False)
    capture_price_wind_offshore_remote: Mapped[float] = mapped_column(nullable=True)
    capture_price_solar: Mapped[float] = mapped_column(nullable=False)
    capture_price_solar_remote: Mapped[float] = mapped_column(nullable=True)
    mw_remote_euro_per_mwh: Mapped[float] = mapped_column(nullable=True)
    pm_remote_euro_per_mwh: Mapped[float] = mapped_column(nullable=True)
    negative_hours_6h: Mapped[str] = mapped_column(nullable=True)
    negative_hours_4h: Mapped[str] = mapped_column(nullable=True)
    negative_hours_3h: Mapped[str] = mapped_column(nullable=True)
    negative_hours_1h: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"<Netztransparenz id={self.id} year={self.year}, month={self.month}>"


class RedispatchMeta(Base):
    """
    Metadata for the 13k energy law data.

    The 13k energy law in Germany refers to a regulation that allows for compensation
    energy adjustments.
    This can result in either an increase or curtailment in energy production
    to maintain grid stability.

    This table stores metadata related to these adjustments, including the source of
    the data and the region
    in which the adjustments took place.

    Attributes:
        id (Mapped[int]): The primary key of the metadata entry.
        source (Mapped[str]): The source from which the data was obtained.
        region (Mapped[str]): The region in which the energy adjustments took place.
        site (Mapped[str]): The site/region_key where the energy adjustments took place
    """

    __tablename__ = "redispatch_meta"

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str]
    region: Mapped[str]
    site: Mapped[str]
    upload_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    data: Mapped["RedispatchData"] = relationship(back_populates="meta")

    __table_args__ = (
        UniqueConstraint("region", "site", name="redispatch_meta_region_site_key"),
    )

    def __repr__(self) -> str:
        return (
            f"<RedispatchMeta id={self.id} source={self.source}, "
            f"upload_date={self.upload_date}>"
        )


class RedispatchData(Base):
    """
    Data for compensation energy adjustments due to the 13k energy law in Germany.

    The 13k energy law allows for adjustments in energy production to maintain
    grid stability. This can result in either an increase or curtailment in energy
    production. This table stores data related to these adjustments, including the time
    of the adjustment, the amount of increase or curtailment, the date the data was
    uploaded to the external database, and the region within the transmission area
    where the adjustment took place.

    Attributes:
        id (int): The id of the dataset
        timestamp (datetime): The time at which the energy adjustment took place.
        increase (float): The amount of energy increase due to the 13k law, if any.
        curtailment (float): The amount of energy curtailment due to the 13k law,
            if any.
        upload_date (datetime): The date the data was uploaded to the external database.
        region_key (int): The key of the region within the transmission area where
            the adjustment took place.
    """

    __tablename__ = "redispatch_data"
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )
    increase: Mapped[float]
    curtailment: Mapped[float]
    region_key: Mapped[int] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(primary_key=True)

    meta_id: Mapped[int] = mapped_column(
        ForeignKey("redispatch_meta.id"), primary_key=True
    )

    meta: Mapped["RedispatchMeta"] = relationship(back_populates="data")


class InflationMeta(Base):
    """
    Table containing inflation metadata.

    :param int id: Primary key.
    :param str source: source of the inflation data
    :param str name: specific name of the inflation data
    :param datetime min_datetime: start date of the data
    :param datetime max_datetime: end date of the data
    :param datetime computed_at: date of the data creation
    """

    __tablename__ = "inflation_meta"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    source: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    min_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    max_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    computed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    description: Mapped[str] = mapped_column(nullable=True)

    data: Mapped["InflationData"] = relationship(back_populates="meta")

    def __repr__(self) -> str:
        return f"<InflationMeta id={self.id}, source={self.source}>"


class InflationData(Base):
    """
    Table containing inflation data.

    :param datetime timestamp: timestamp of the inflation value.
    :param float value: inflation value
    :param int meta_id: meta_id of the inflation data
    """

    __tablename__ = "inflation_data"

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )
    value: Mapped[float] = mapped_column(nullable=False)
    meta_id: Mapped[int] = mapped_column(
        ForeignKey("inflation_meta.id"), primary_key=True
    )

    meta: Mapped["InflationMeta"] = relationship(back_populates="data")

    def __repr__(self) -> str:
        return f"<Inflation timestamp={self.timestamp}, value={self.value}>"
