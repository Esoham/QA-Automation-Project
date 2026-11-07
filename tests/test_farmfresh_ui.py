"""Real Chromium E2E browser testing of the legacy Flask app."""
import os
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

import pytest
from playwright.sync_api import expect, sync_playwright

pytestmark = pytest.mark.ui


@pytest.fixture(scope="module")
def farmfresh_url():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    url = f"http://127.0.0.1:{port}"
    process = subprocess.Popen(
        [sys.executable, "-m", "flask", "--app", "app", "run", "--host", "127.0.0.1", "--port", str(port)],
        cwd=Path(__file__).resolve().parents[1],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    try:
        for _ in range(100):
            if process.poll() is not None:
                raise RuntimeError("Flask server exited: " + process.stderr.read().decode(errors="replace"))
            try:
                with urlopen(url + "/health", timeout=0.2) as response:
                    if response.status == 200:
                        break
            except (URLError, TimeoutError):
                time.sleep(0.1)
        else:
            raise RuntimeError("FarmFresh did not start within readiness window")
        yield url
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
        if process.stderr:
            process.stderr.close()


@pytest.fixture
def farmfresh_page(farmfresh_url):
    with sync_playwright() as p:
        launch = {"headless": True}
        if os.environ.get("CHROMIUM_PATH"):
            launch["executable_path"] = os.environ["CHROMIUM_PATH"]
        browser = p.chromium.launch(**launch)
        context = browser.new_context(base_url=farmfresh_url)
        page = context.new_page()
        try:
            yield page
        finally:
            context.close()
            browser.close()


def test_farmfresh_product_catalog_search_and_categories(farmfresh_page):
    page = farmfresh_page
    page.goto("/products")
    expect(page.get_by_role("heading", name="Our Products")).to_be_visible()
    expect(page.locator(".product-card")).to_have_count(4)
    page.get_by_role("searchbox", name="Search products").fill("cheese")
    expect(page.locator(".product-card")).to_have_count(1)
    expect(page.get_by_role("link", name="Artisanal Cheese")).to_be_visible()
    page.get_by_role("searchbox", name="Search products").fill("")
    page.get_by_role("combobox", name="Product category").select_option("Dairy")
    expect(page.locator(".product-card")).to_have_count(2)


def test_farmfresh_empty_search_and_navigation(farmfresh_page):
    page = farmfresh_page
    page.goto("/products")
    page.get_by_role("searchbox", name="Search products").fill("no-such-item")
    expect(page.get_by_text("No products match your search.")).to_be_visible()
    page.get_by_role("link", name="About", exact=True).click()
    expect(page.get_by_role("heading", name="About FarmFresh Tester")).to_be_visible()


def test_farmfresh_demo_cart_changes_and_clears(farmfresh_page):
    page = farmfresh_page
    page.goto("/products")
    expect(page.locator("#cart-status")).to_have_text("Cart: 0 items — $0.00")
    page.get_by_role("button", name="Add Organic Apples to cart").click()
    expect(page.locator("#cart-status")).to_have_text("Cart: 1 item — $2.99")
    page.get_by_role("button", name="Add Free-range Eggs to cart").click()
    expect(page.locator("#cart-status")).to_have_text("Cart: 2 items — $7.49")
    page.get_by_role("button", name="Clear cart").click()
    expect(page.locator("#cart-status")).to_have_text("Cart: 0 items — $0.00")


def test_farmfresh_detail_page_and_safe_search(farmfresh_page):
    page = farmfresh_page
    page.goto("/products")
    page.get_by_role("link", name="Organic Apples").click()
    expect(page.get_by_role("heading", name="Organic Apples")).to_be_visible()
    page.get_by_role("link", name="Back to products").click()
    page.get_by_role("searchbox", name="Search products").fill("<img src=x onerror=alert(1)>")
    expect(page.get_by_text("No products match your search.")).to_be_visible()
    assert page.locator("img").count() == 0
