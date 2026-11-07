"""API, data contract, business rule, security-negative and boundary tests."""
import pytest


def test_catalog_contract(api):
    result = api.get("/api/products")
    assert result.status_code == 200
    body = result.json()
    assert body["count"] == 6
    assert body["count"] == len(body["items"])
    assert all(set(["sku", "name", "specification", "stock", "unit_price", "category"]) <= set(p) for p in body["items"])


@pytest.mark.parametrize("search,expected", [("m6", 3), ("  BOLT-m6  ", 1), ("nitrile", 1), ("not-found", 0), ("<script>alert(1)</script>", 0)])
def test_search_and_invalid_input_are_handled(api, search, expected):
    payload = api.get("/api/products", params={"search": search}).json()
    assert payload["count"] == expected


def test_filter_category(api):
    data = api.get("/api/products", params={"category": "Fasteners"}).json()
    assert data["count"] == 3
    assert {x["category"] for x in data["items"]} == {"Fasteners"}


def test_single_product_and_missing_sku(api):
    assert api.get("/api/products/BOLT-M6").json()["stock"] == 120
    assert api.get("/api/products/DOES-NOT-EXIST").status_code == 404


def test_quote_correct_decimal_arithmetic(api):
    res = api.post("/api/quotes", json={"lines": [{"sku": "BOLT-M6", "quantity": 3}, {"sku": "NUT-M6", "quantity": 2}]})
    assert res.status_code == 200
    assert res.json()["subtotal"] == "1.41"
    assert [x["line_total"] for x in res.json()["lines"]] == ["1.05", "0.36"]


@pytest.mark.parametrize("payload,code", [
    ({"lines": []}, 422),
    ({"lines": [{"sku": "BOLT-M6", "quantity": 0}]}, 422),
    ({"lines": [{"sku": "BOLT-M6", "quantity": -1}]}, 422),
    ({"lines": [{"sku": "BOLT-M6", "quantity": 121}]}, 409),
    ({"lines": [{"sku": "GLOVE-N", "quantity": 1}]}, 409),
    ({"lines": [{"sku": "UNKNOWN", "quantity": 1}]}, 404),
    ({"lines": [{"sku": "BOLT-M6", "quantity": 1}, {"sku": "BOLT-M6", "quantity": 1}]}, 422),
])
def test_quote_failure_modes(api, payload, code):
    assert api.post("/api/quotes", json=payload).status_code == code


def test_search_enforces_length_limit(api):
    assert api.get("/api/products", params={"search": "x" * 101}).status_code == 422
