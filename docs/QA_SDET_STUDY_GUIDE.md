# QA / SDET comeback plan — Playwright, Selenium, APIs and AI testing

Goal: demonstrate independent, reproducible QA engineering skills for interviews. This project does not equate to 3–5 years of professional experience. Speak accurately about actual employment history and the portfolio's synthetic scope.

Study cadence: four 40-minute sessions each week. Every session: (1) make a hypothesis; (2) run or change code; (3) inspect a failure; (4) explain the result without reading a script.

## Week 1 — Python, pytest and API contracts
- Read commerceqa/main.py and tests/test_api.py. Trace a customer's product lookup and quote from request to response.
- Run: python -m pytest tests/test_api.py -q
- Study 200 vs 404 vs 409 vs 422, boundary values, decimal arithmetic, parameterized tests and test isolation.
- Exercise: write a failing test for a quote above available stock. Fix the defect on a practice branch; demonstrate the red-to-green cycle.
- Interview drill: Why is an API contract test not the same as a browser end-to-end test?

## Week 2 — Playwright
- Read tests/conftest.py and tests/test_ui.py; run: python -m pytest -m ui -q
- Learn user-facing locators (get_by_role), auto-waiting assertions, isolation, browser traces and debugging.
- Exercise: add a UI regression test for an empty search and explain what would make it flaky.
- Interview drill: Explain why stable accessibility-based locators outperform positional CSS/XPath.

## Week 3 — Selenium 4 and Page Object Model
- Read selenium_pages/catalog_page.py and tests/test_selenium.py; run: python -m pytest -m selenium -q
- Study WebDriver session lifecycle, explicit waits, expected conditions, Page Objects and stale elements.
- Exercise: add a Selenium empty-results test and compare it with the Playwright version.
- Interview drill: Explain the different waiting/driver models and how to diagnose flaky CI tests.

## Week 4 — AI evaluation, CI and interview presentation
- Read evals/golden_cases.json, evals/grade.py and tests/test_ai_eval.py.
- Run: python -m evals.grade. Change a sample output to invent a SKU or claim nonexistent stock, and verify the grader rejects it.
- Review .github/workflows/commerceqa-ci.yml plus actual GitHub Actions JUnit and trace artifacts.
- Practice a five-minute talk: customer risk → test strategy → implementation → CI result → limitations and next improvements.
- Interview drill: Explain why 8/8 curated fixtures is NOT a benchmark of real AI model accuracy.

## Work sample checklist
- Independently write and explain two API tests, two Playwright tests, two Selenium tests and one AI evaluator negative test.
- Be able to debug a genuine failed assertion using logs, trace, HTTP status and test data.
- Explain severity vs priority, smoke vs regression vs integration testing, and test pyramid trade-offs.
- Describe what the project does NOT include: no real customers, payment or shipping integration, verified production security, or live-model accuracy.
- Frame the old Pitney Bowes QA work truthfully and keep it separate from later independent Python testing.

## Technical reference links
- Playwright locators: https://playwright.dev/python/docs/locators
- Playwright best practices: https://playwright.dev/docs/best-practices
- Selenium waits: https://www.selenium.dev/documentation/webdriver/waits/
- Selenium page object models: https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/
- OpenAI evaluation best practices: https://developers.openai.com/api/docs/guides/evaluation-best-practices
