from datetime import datetime, timezone

from sqlalchemy import (
    String,
    Float,
    Integer,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from database.base import Base


class Competitor(Base):
    __tablename__ = "competitors"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    website: Mapped[str] = mapped_column(String(255), nullable=False)

    country: Mapped[str] = mapped_column(String(100), nullable=False)

    prices = relationship(
        "Price",
        back_populates="competitor"
    )

    snapshots = relationship(
        "DailySnapshot",
        back_populates="competitor"
    )

    def __repr__(self):
        return f"<Competitor {self.name}>"



class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)

    product_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    brand: Mapped[str] = mapped_column(
        String(100)
    )

    category: Mapped[str] = mapped_column(
        String(100)
    )

    sku: Mapped[str] = mapped_column(
        String(100),
        unique=True
    )

    prices = relationship(
        "Price",
        back_populates="product"
    )

    snapshots = relationship(
        "DailySnapshot",
        back_populates="product"
    )

    def __repr__(self):
        return f"<Product {self.product_name}>"



class Price(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id")
    )

    competitor_id: Mapped[int] = mapped_column(
        ForeignKey("competitors.id")
    )

    price: Mapped[float] = mapped_column(Float)

    currency: Mapped[str] = mapped_column(
        String(10)
    )

    discount: Mapped[float] = mapped_column(Float)

    captured_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    product = relationship(
        "Product",
        back_populates="prices"
    )

    competitor = relationship(
        "Competitor",
        back_populates="prices"
    )



class DailySnapshot(Base):
    __tablename__ = "daily_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id")
    )

    competitor_id: Mapped[int] = mapped_column(
        ForeignKey("competitors.id")
    )

    rating: Mapped[float] = mapped_column(Float)

    reviews: Mapped[int] = mapped_column(Integer)

    stock_status: Mapped[str] = mapped_column(
        String(50)
    )

    shipping_cost: Mapped[float] = mapped_column(Float)

    exchange_rate: Mapped[float] = mapped_column(Float)

    capture_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    product = relationship(
        "Product",
        back_populates="snapshots"
    )

    competitor = relationship(
        "Competitor",
        back_populates="snapshots"
    )