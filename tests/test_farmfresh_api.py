"""Black-box HTTP tests and boundary-value analysis for the restored Flask catalog."""
import pytest
from app import app


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def test_critical_pages_available(client):
    for path, expected in (("/", b"Welcome to FarmFresh Tester"),
                           ("/products", b"Our Products"),
                           ("/about", b"About FarmFresh Tester")):
        response = client.get(path)
        assert response.status_code == 200, path
        assert expected in response.data


def test_catalog_contract_and_stable_ids(client):
    response = client.get("/api/products")
    assert response.status_code == 200
    assert response.content_type.startswith("application/json")
    items = response.get_json()
    assert len(items) == 4
    assert len({item["id"] for item in items}) == len(items)
    assert all({"id", "name", "description", "price", "origin", "category"} <= set(item) for item in items)


@pytest.mark.parametrize("search,count", [
    ("apples", 1), ("EGGS", 1), ("  beef  ", 1), ("unknown", 0),
    ("<script>alert(1)</script>", 0), ("", 4),
])
def test_search_equivalence_partitions(client, search, count):
    response = client.get("/api/products", query_string={"search": search})
    assert response.status_code == 200
    assert len(response.get_json()) == count


@pytest.mark.parametrize("category,count", [
    ("Dairy", 2), ("dairy", 2), ("Fruits", 1), ("unknown", 0), ("", 4),
])
def test_category_filter(client, category, count):
    response = client.get("/api/products", query_string={"category": category})
    assert len(response.get_json()) == count


def test_combined_search_and_filter(client):
    response = client.get("/api/products", query_string={"search": "Cheese", "category": "Dairy"})
    assert [item["id"] for item in response.get_json()] == [4]


@pytest.mark.parametrize("length,status", [(99, 200), (100, 200), (101, 400)])
def test_search_boundary(client, length, status):
    response = client.get("/api/products", query_string={"search": "x" * length})
    assert response.status_code == status


def test_category_length_validation(client):
    assert client.get("/api/products", query_string={"category": "x" * 41}).status_code == 400


def test_product_detail_and_missing_id(client):
    data = client.get("/api/products/1")
    assert data.status_code == 200
    assert data.get_json()["name"] == "Organic Apples"
    assert client.get("/api/products/999").status_code == 404
    assert client.get("/product/999").status_code == 404


def test_health_check(client):
    assert client.get("/health").get_json() == {"status": "ok"}
