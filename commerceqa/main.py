"""Synthetic industrial catalog used as a reproducible software QA test target."""
from decimal import Decimal
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

app = FastAPI(title="CommerceQA Test Storefront", version="1.0.0")
SITE = Path(__file__).parent / "index.html"

# Fictional SKU catalog: no real merchants, customers, or proprietary product data.
PRODUCTS = (
    {"sku": "BOLT-M6", "name": "M6 Hex Bolt", "category": "Fasteners", "specification": "M6 x 20 mm, zinc-plated steel", "unit_price": "0.35", "stock": 120},
    {"sku": "NUT-M6", "name": "M6 Hex Nut", "category": "Fasteners", "specification": "M6, zinc-plated steel", "unit_price": "0.18", "stock": 300},
    {"sku": "CLAMP-25", "name": "Tube Clamp", "category": "Hardware", "specification": "25 mm nominal diameter", "unit_price": "2.45", "stock": 34},
    {"sku": "GLOVE-N", "name": "Nitrile Work Gloves", "category": "Safety", "specification": "Powder-free, size L, box of 100", "unit_price": "11.50", "stock": 0},
    {"sku": "TAPE-EL", "name": "Electrical Tape", "category": "Electrical", "specification": "PVC, 19 mm x 20 m, black", "unit_price": "3.10", "stock": 80},
    {"sku": "WASH-M6", "name": "M6 Flat Washer", "category": "Fasteners", "specification": "M6, stainless steel", "unit_price": "0.12", "stock": 500},
)
INDEX = {p["sku"]: p for p in PRODUCTS}


class QuoteLine(BaseModel):
    sku: str = Field(min_length=1, max_length=40)
    quantity: int = Field(ge=1, le=10000)


class QuoteRequest(BaseModel):
    lines: list[QuoteLine] = Field(min_length=1, max_length=20)


@app.get("/", include_in_schema=False)
def storefront():
    return FileResponse(SITE, media_type="text/html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/products")
def products(search: Annotated[str, Query(max_length=100)] = "", category: Annotated[str, Query(max_length=50)] = ""):
    term = search.strip().casefold()
    kind = category.strip().casefold()
    matches = [p for p in PRODUCTS if (
        not term or any(term in str(p[field]).casefold() for field in ("sku", "name", "specification"))
    ) and (not kind or p["category"].casefold() == kind)]
    return {"items": matches, "count": len(matches)}


@app.get("/api/products/{sku}")
def product(sku: str):
    found = INDEX.get(sku.upper())
    if not found:
        raise HTTPException(status_code=404, detail="Product not found")
    return found


@app.post("/api/quotes")
def quote(request: QuoteRequest):
    seen = set()
    prepared = []
    subtotal = Decimal("0.00")
    for line in request.lines:
        sku = line.sku.upper()
        if sku in seen:
            raise HTTPException(status_code=422, detail="Duplicate SKU in quote")
        seen.add(sku)
        found = INDEX.get(sku)
        if not found:
            raise HTTPException(status_code=404, detail=f"Unknown SKU: {sku}")
        if line.quantity > found["stock"]:
            raise HTTPException(status_code=409, detail=f"Insufficient stock for {sku}")
        extended = Decimal(found["unit_price"]) * line.quantity
        subtotal += extended
        prepared.append({"sku": sku, "quantity": line.quantity, "line_total": f"{extended:.2f}"})
    return {"lines": prepared, "subtotal": f"{subtotal:.2f}", "currency": "USD"}
