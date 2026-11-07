# Local verification evidence — November 6, 2026

- Command: `CHROMIUM_PATH=/usr/bin/chromium QA_INPROCESS=1 python -m pytest -q --junitxml=evidence/local-junit.xml`
- Outcome: **27 tests passed** locally, including six Playwright/Chromium UI tests.
- Chromium environment caveat: this tool runtime prevents normal URL navigation (`ERR_BLOCKED_BY_ADMINISTRATOR`). `QA_INPROCESS=1` renders the actual browser UI and intercepts its HTTP API requests with FastAPI's deterministic TestClient. This is not equivalent to a full deployed HTTP-stack browser run.
- The GitHub Actions workflow is configured to run the ordinary local-web-server browser path (`QA_INPROCESS` off); it must pass CI before claiming complete end-to-end coverage.
- AI command: `python -m evals.grade --report evidence/local-ai-eval-report.json`.
- Outcome: **8/8 curated synthetic candidate outputs meet their authored expected results**. This does **not** measure a live AI model's accuracy. Negative evaluator tests also pass and confirm malformed or hallucinated outputs are rejected.
