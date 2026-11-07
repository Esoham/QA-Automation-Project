# AI-assisted engineering: design, implement, verify, observe

## Problem statement
A QA hiring manager needs verifiable evidence of engineering judgment, not a claim that AI wrote test scripts. Older FarmFresh repository files contain mismatched/incomplete tests and no verified CI pipeline. This upgrade adds a **standalone, deterministic QA lab** without deleting legacy work.

## Working method
1. **Define success before generating code.** Cover customer-facing product search and quote behavior, API contracts, negative/boundary cases, and AI-generated response risk.
2. **Build the smallest controllable system.** A fictional industrial catalog gives reproducible fixtures without depending on third-party website changes or real customer data.
3. **Use AI as an assistant, not an oracle.** Generate hypotheses, possible edge cases, implementations, and review checklists. Independently examine the logic, run code, and inspect failed cases.
4. **Test at the right layer.** FastAPI TestClient checks data contracts and business rules; Playwright tests actual user-visible workflows; the separate eval runner checks structured AI responses against human-curated expectations.
5. **Observe and improve.** Record JUnit results and Playwright traces; when a regression is found, add a failing test before fixing it. Use small pull requests, code review, and CI gates.

## AI evaluation scope
- Eight synthetic prompt/response pairs, covering correct SKU recommendation, product specifications, out-of-stock truthfulness, unsupported products, high-stakes advice, and prompt injection.
- Deterministic metrics: expected recommendation set, correct refusal flag, known SKUs, and catalog-grounded structured facts.
- Negative tests intentionally modify a response and verify that the evaluator fails it.
- Feed real model outputs through `python -m evals.grade --candidate path/to/model-outputs.json` when available. No AI provider, model call, or API key is required for CI.
- The sample outputs are **curated fixtures**, not measured model performance. Pass rate on fixtures must never be advertised as live AI accuracy. Text not structured as product claims still requires human semantic review; the simplistic secret substring check does not establish robust security.

## Human review checklist
- [ ] Compare expected outcomes with requirements, not with implementation details.
- [ ] Check invented SKUs, wrong availability, false specifications, prompt injection, and sensitive-data disclosure.
- [ ] Review test isolation, locator stability, API error codes, and quote arithmetic.
- [ ] Inspect trace artifacts for UI failures; don't just re-run flaky tests until green.
- [ ] Add a real-model evaluation dataset before making claims about provider quality.

## Source-informed choices
- GitHub (Nov 2026): Plan → Build → Verify → Observe for AI-assisted engineering.
- Playwright official best practices: isolated tests, user-visible locators, web-first assertions, and CI trace analysis.
- OpenAI evaluation best practices: task-specific gold datasets, automated grading, adversarial cases, human calibration, continuous evaluation.
