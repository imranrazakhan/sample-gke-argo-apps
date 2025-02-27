from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from datetime import datetime
from typing import Optional
from .base import Base


class H2PricingMeta(Base):
    """Table containing the meta data for the H2 pricing tables."""

    __tablename__ = "h2_pricing_meta"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    computed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    name: Mapped[str]
    comment: Mapped[Optional[str]]

    h2_pricing_relation: Mapped["H2Pricing"] = relationship(
        back_populates="h2_pricing_meta_relation"
    )


class H2Pricing(Base):
    """Holds the H2 prices over multiple years for different model scenarios."""

    __tablename__ = "h2_pricing"

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), primary_key=True
    )
    meta_id: Mapped[int] = mapped_column(
        ForeignKey("h2_pricing_meta.id"), primary_key=True
    )
    h2_price: Mapped[float]

    h2_pricing_meta_relation: Mapped["H2PricingMeta"] = relationship(
        back_populates="h2_pricing_relation"
    )
