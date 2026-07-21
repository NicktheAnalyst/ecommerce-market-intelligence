import pytest
from database.base import Base
from database.connection import engine
from database.crud import create_competitor, create_product, create_price
from analysis.data_loader import DataLoader


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Fixture to ensure a clean database state before running tests."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_crud_operations():
    """Test standard CRUD operations for competitors, products, and prices."""
    comp = create_competitor("Test Corp", "https://test.com", "Kenya")
    assert comp.id is not None
    assert comp.name == "Test Corp"

    prod = create_product("Test Phone", "TestBrand", "Tech", "TEST-SKU-123")
    assert prod.id is not None
    assert prod.sku == "TEST-SKU-123"

    price = create_price(prod.id, comp.id, 50000, "KES", 5)
    assert price.id is not None
    assert price.price == 50000


def test_data_loader():
    """Test DataLoader integration to confirm DataFrames fetch seeded data."""
    loader = DataLoader()

    products_df = loader.load_products()
    prices_df = loader.load_prices()
    competitors_df = loader.load_competitors()

    assert not products_df.empty
    assert not prices_df.empty
    assert not competitors_df.empty

    assert products_df.iloc[0]["sku"] == "TEST-SKU-123"
    assert competitors_df.iloc[0]["name"] == "Test Corp"