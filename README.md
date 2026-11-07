# CommerceQA — Software Test Automation & AI Evaluation Lab

**Portfolio upgrade of the FarmFresh Tester exercise** | Python · Playwright · pytest · FastAPI · GitHub Actions

A working QA engineering portfolio lab built around a **fictional B2B industrial catalog**. It demonstrates browser automation, HTTP API testing, regression suites, negative/boundary tests, basic security checks, and AI-response evaluations. This is a test fixture, **not** a commercial e-commerce service or a deployed AI model.

## Two real QA practice applications in this repository

**FarmFresh Tester (restored original Flask app):** Search and filter a fictional food catalog, view product detail pages and use a visible local cart. The original broken links and stale tests have been repaired. Product data is rendered with safe text DOM APIs rather than interpolated into innerHTML. Run locally with `python -m flask --app app run`, then open `http://127.0.0.1:5000/products`.

**CommerceQA (new B2B industrial demo):** Playwright + Selenium + API testing and an offline AI-answer evaluation harness. See instructions below.

FarmFresh tests live in `tests/test_farmfresh_api.py` and `tests/test_farmfresh_ui.py`; historical root smoke tests (`test_routes.py`, `test_app.py`) are also fixed and can be run explicitly. The CI suite runs FarmFresh and CommerceQA together. See [FarmFresh Agile sprint, acceptance criteria, and defect log](docs/FARMFRESH_SPRINT_AND_TEST_STRATEGY.md).

## Business scenario
An industrial buyer must find the correct component by part number or specification, check stock, and request an accurate quote. Errors could cause a wrong-part purchase, delayed job, or misleading availability promise. This QA suite aims to detect those errors before release.

## Tested features and risk coverage

| Layer | What is verified | Representative risk |
| --- | --- | --- |
| Browser / Playwright | Accessible search, filters, empty states, quote success/error, malicious-looking input | Buyer sees incorrect information or a broken flow |
| API / pytest | Data contract, matching/filters, product lookup, decimal totals, invalid quantities, duplicates, stock shortages | Incorrect product data or an impossible order |
| AI evaluation | Golden prompts, structured grounding, refusal, unknown SKUs, adversarial prompt, evaluator-negative tests | Hallucinated product/spec or unsupported recommendation |
| CI / GitHub Actions | Repeatable test run, JUnit artifacts, Playwright traces, eval JSON report | Regression not detected or failure hard to reproduce |

## Run locally

Use Python 3.11+ in a clean virtual environment:

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows: .venv\Scripts\activate
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
python -m pytest -q
python -m evals.grade --report results/ai-eval-report.json
```

Start the demo storefront with:

```bash
python -m uvicorn commerceqa.main:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/` or inspect API documentation at `http://127.0.0.1:8000/docs`.

Run only the Playwright suite with `python -m pytest -m ui -q`, or only non-browser cases with `python -m pytest -m "not ui" -q`. Browser tests always target a localhost fixture and never submit data to external services. To use an existing system Chromium binary, set `CHROMIUM_PATH` to its full path.


## Selenium 4 WebDriver comparison

The repository also demonstrates Chrome WebDriver and Page Object Model:
`selenium_pages/catalog_page.py` centralizes navigation and explicit waits,
and `tests/test_selenium.py` checks search, quote prices and stock exceptions.
Each test uses a fresh browser. No fixed sleeps; assertions remain in the tests.

Run: `python -m pytest -m selenium -q`.
On a workstation Selenium Manager may configure ChromeDriver; in CI a separate job uses preinstalled Chrome and Selenium Manager. Do not call Selenium
tests verified until that CI check succeeds.

See [the 4-week QA/SDET study plan](docs/QA_SDET_STUDY_GUIDE.md).

## AI-testing portfolio evidence

`evals/golden_cases.json` contains eight **human-curated synthetic** test cases; `evals/sample_model_outputs.json` is a matching set of **manually authored example outputs**. The evaluator validates product citations and structured claims. Run it against your own model response file with:

```bash
python -m evals.grade --candidate path/to/your_model_outputs.json --report results/model-eval.json
```

For each ID, submit `recommended_skus` (strings), `refused` (boolean), `answer` (string), and `product_claims` (optional array of `{ "sku": ..., "field": ..., "value": ... }`). There is **no live LLM client or verified provider accuracy** in this repository. Open-ended natural-language claims require separate human review.

## Evidence and caveats

- `tests/test_api.py`: repeatable API/contract/boundary tests.
- `tests/test_ui.py`: actual Chromium browser workflows with Playwright locators and trace capture.
- `tests/test_ai_eval.py`: proof the grader detects deliberately corrupted AI responses.
- `.github/workflows/commerceqa-ci.yml`: automated verification and downloadable test artifacts.
- `docs/AI_ENGINEERING_WORKFLOW.md`: design decisions, risks and evaluation policy.
- `docs/INTEGRATING_WITH_ORIGINAL_REPO.md`: safe branch/PR instructions for upgrading the original GitHub repository.
- Synthetic inventory only; no real customer, payment, shipping, safety certification, third-party integrations, or production security claims.

For test-environment limitations and recorded local evidence, see `evidence/LOCAL_VERIFICATION.md`. In restricted browser environments, set `QA_INPROCESS=1` to test the actual Chromium-rendered UI against an in-process HTTP mock; normal CI does not use that mode.

### Portfolio-ready summary

> Built an independent automated QA lab for a synthetic B2B product catalog, validating browser purchase-discovery workflows with Playwright, API contracts and edge cases with pytest, and structured AI assistant outputs using gold-standard and adversarial evaluation cases. Added GitHub Actions regression execution with test reports and browser traces.
