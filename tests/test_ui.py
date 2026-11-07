"""Playwright UI, accessibility semantics and cross-layer workflow checks."""
import pytest
from playwright.sync_api import expect
from pathlib import Path
import os


def open_store(page):
    if os.environ.get("QA_INPROCESS") == "1":
        source = (Path(__file__).resolve().parents[1] / "commerceqa/index.html").read_text()
        page.set_content(source.replace("</head>", '<base href="http://demo.test/"></head>'))
    else:
        page.goto("/")

pytestmark = pytest.mark.ui


def test_catalog_loads_with_accessible_controls(browser_page):
    page = browser_page
    open_store(page)
    expect(page.get_by_role("heading", name="CommerceQA Industrial Parts")).to_be_visible()
    expect(page.get_by_role("textbox", name="Search products")).to_be_visible()
    expect(page.get_by_role("combobox", name="Category")).to_be_visible()
    expect(page.get_by_role("status").first).to_have_text("6 products found")
    expect(page.get_by_role("article")).to_have_count(6)


def test_search_and_category_filter(browser_page):
    page = browser_page
    open_store(page)
    page.get_by_role("textbox", name="Search products").fill("m6")
    page.get_by_role("combobox", name="Category").select_option("Fasteners")
    page.get_by_role("button", name="Search products").click()
    expect(page.get_by_role("status").first).to_have_text("3 products found")
    expect(page.get_by_role("article")).to_have_count(3)


def test_no_results_uses_helpful_message(browser_page):
    page = browser_page
    open_store(page)
    page.get_by_role("textbox", name="Search products").fill("inexistent")
    page.get_by_role("textbox", name="Search products").press("Enter")
    expect(page.get_by_text("No products match your search.")).to_be_visible()


def test_customer_can_request_quote(browser_page):
    page = browser_page
    open_store(page)
    page.get_by_role("button", name="Quote BOLT-M6").click()
    expect(page.get_by_text("Quote for BOLT-M6: $0.35")).to_be_visible()


def test_out_of_stock_quote_shows_clear_error(browser_page):
    page = browser_page
    open_store(page)
    page.get_by_role("button", name="Quote GLOVE-N").click()
    expect(page.get_by_text("Quote unavailable: Insufficient stock for GLOVE-N")).to_be_visible()


def test_search_does_not_execute_markup(browser_page):
    page = browser_page
    open_store(page)
    page.get_by_role("textbox", name="Search products").fill("<img src=x onerror=alert(1)>")
    page.get_by_role("button", name="Search products").click()
    expect(page.get_by_text("No products match your search.")).to_be_visible()
    assert page.locator("img").count() == 0
