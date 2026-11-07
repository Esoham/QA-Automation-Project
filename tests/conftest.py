"""Fixtures keep browser tests isolated and run only against the local demo."""
import os
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen
from urllib.parse import urlsplit

import pytest
from fastapi.testclient import TestClient
from commerceqa.main import app, SITE


@pytest.fixture
def api():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def server_url():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    url = f"http://127.0.0.1:{port}"
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "commerceqa.main:app", "--host", "127.0.0.1", "--port", str(port)],
        cwd=Path(__file__).resolve().parents[1], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
    )
    try:
        for _ in range(90):
            if proc.poll() is not None:
                raise RuntimeError(f"Demo server exited: {proc.stderr.read().decode(errors='replace')}")
            try:
                with urlopen(url + "/health", timeout=0.3) as response:
                    if response.status == 200:
                        break
            except (URLError, TimeoutError):
                time.sleep(0.1)
        else:
            raise RuntimeError("Demo server did not become healthy")
        yield url
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)
        if proc.stderr:
            proc.stderr.close()


@pytest.fixture
def browser_page(server_url, tmp_path, request):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as playwright:
        kwargs = {"headless": True}
        executable = os.environ.get("CHROMIUM_PATH")
        if executable:
            kwargs["executable_path"] = executable
        browser = playwright.chromium.launch(**kwargs)
        context = browser.new_context(base_url=server_url, viewport={"width": 1280, "height": 900})
        page = context.new_page()
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        try:
            if os.environ.get("QA_INPROCESS") == "1":
                # Local browser policies sometimes prohibit all URL navigation.
                # Test real UI JavaScript with a mocked network boundary instead.
                with TestClient(app) as test_client:
                    def handle_api(route):
                        parsed = urlsplit(route.request.url)
                        target = parsed.path + ("?" + parsed.query if parsed.query else "")
                        response = test_client.request(route.request.method, target,
                            content=route.request.post_data,
                            headers={"content-type": "application/json"} if route.request.post_data else {})
                        route.fulfill(status=response.status_code, body=response.content,
                            headers={"content-type": response.headers.get("content-type", "application/json"),
                                     "access-control-allow-origin": "*"})
                    page.route("**/api/**", handle_api)
                    yield page
            else:
                yield page
        finally:
            safe_name = request.node.name.replace("/", "_")
            trace_dir = Path(os.environ.get("QA_ARTIFACTS", str(tmp_path)))
            trace_dir.mkdir(exist_ok=True, parents=True)
            context.tracing.stop(path=str(trace_dir / f"{safe_name}.zip"))
            context.close()
            browser.close()
