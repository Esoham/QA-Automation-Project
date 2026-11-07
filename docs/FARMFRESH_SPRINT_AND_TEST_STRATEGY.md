# FarmFresh | Agile feature story, QA plan, and defect notes

## Product and constraints
FarmFresh is a fictional browser catalog for QA practice. Intended users browse items and add them to a **local, temporary cart**. No checkout, account, payment or real fulfillment is supported. Do not claim production customers or commercial use.

### User story FF-01 — Search and filter the catalog
As a buyer, I want to search by product name or description and filter by category, so I can find a relevant item quickly.

**Acceptance criteria**
- AC1: Opening Products shows all four seeded items, with accurate names, prices and descriptions.
- AC2: Search ignores case and surrounding whitespace, and combines correctly with category filtering.
- AC3: Unknown searches show a helpful empty result rather than an error.
- AC4: Product names are inserted into the page as text, never executed as markup.
- AC5: Details links open the correct item; missing item IDs have a visible 404 state.

### User story FF-02 — Experiment with a local cart
As a buyer, I want a clear confirmation when I add a catalog item, so I can understand my current simulated total.

**Acceptance criteria**
- AC6: Adding an item increases the cart count and the correct subtotal.
- AC7: Clearing the cart resets the count and total.
- AC8: The page clearly explains that no payment/order is submitted.

## Risk-based test approach
| Priority | Risk | Verification | Type |
|---|---|---|---|
| High | Customer sees wrong item | Item IDs, combined search/filter, details | API + UI functional |
| High | Incorrect displayed total | Two-product subtotal, clear cart | UI + boundary |
| High | Unsafe HTML injection | DOM text sink, adversarial search | Security negative |
| Medium | Broken navigation | Home, Products, About and missing detail | Smoke/system |
| Medium | Stale filters after rapid typing | Abort previous API request in UI | Design mitigation; follow-up stress scenario |

## Traceability
- AC1, AC2, AC3 → tests/test_farmfresh_api.py and tests/test_farmfresh_ui.py.
- AC4 → static/catalog.js safe text construction and UI adversarial search test.
- AC5 → Flask detail-route tests and Playwright navigation.
- AC6, AC7, AC8 → browser cart test and visible demo disclaimer.

## Testing layers and how to think
- **Black box:** Send API inputs and verify HTTP codes/JSON without needing code internals.
- **Gray box:** Compare actual client behavior with server validation and data transformations.
- **White box:** Review the search predicate, request cancellation and DOM construction paths; add targeted unit tests if expanded.
- **Smoke:** Pages respond, catalog loads and navigation is usable.
- **Regression:** Run API + Playwright + CommerceQA automation after changes to prevent existing features from breaking.
- **Retest:** Rerun the single failing case after fixing a specific defect before running regression.
- **Exploratory:** Investigate keyboard-only filtering, slow connections, duplicate click behavior, reload/reset, and unexpected strings.

## Reproduced issues repaired in this change
- **FF-BUG-01 | Medium:** About navigation pointed to missing route. Added an About endpoint and template, with route/UI coverage.
- **FF-BUG-02 | Medium:** Historical smoke tests asserted the wrong home text or nonexistent About route. Aligned tests with product behavior.
- **FF-BUG-03 | Medium:** "Add to Cart" displayed only an alert rather than changing cart state. Replaced with visible count/subtotal and clear action.
- **FF-BUG-04 | High potential security risk:** Product-card markup previously interpolated API product strings into innerHTML and inline JS. New rendering uses createElement and textContent. Test coverage is limited to controlled demo scenarios, not a security audit.
- **FF-BUG-05 | Low:** Original static stylesheet lived under templates/static, outside Flask's default static URL. Added a served static stylesheet.

## Release decision
Before merging: verify the existing CommerceQA jobs plus the repaired FarmFresh Flask API and Chromium UI tests are green in GitHub Actions. Report the exact verified test count; do not claim tests outside this repository or real customer performance.
