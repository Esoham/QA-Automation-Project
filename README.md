# FarmFresh Tester — Flask & Software QA Exercises

**Status: early-stage QA practice project, not a verified production-ready automation framework.**

This repository contains a sample **Flask product catalog**, Jinja templates, an `/api/products` filtering endpoint, several pytest-style test files, and exploratory files for UI/API testing and performance testing.

## Start here
- [Flask app and API routes](app.py)
- [Route tests](test_routes.py) and [additional test](test_app.py)
- [Product UI with search/category filtering](templates/products.html)
- [Sample dependency list](updated-requirements-flask.txt)

## Run the sample application (not independently verified)

```bash
python -m venv .venv
# Activate your environment for your OS
pip install -r updated-requirements-flask.txt
python app.py
```

The Flask development server is for local use, **not public hosting**.

## Known limitations

- The tests have not been confirmed to pass. Some assertions mismatch the current app (for example, a test expects an undefined `/about` route).
- Several alternate config/test examples are mixed together; they have not been consolidated into a single verified pipeline.
- Local virtual-environment, cache, and coverage artifacts are present in the repository and should be reviewed before removal.
- There are no verified deployment, coverage, or load-test outcomes to report.

## Next cleanup tasks
1. Align route assertions with the implementation, add API positive/negative test cases, and run them.
2. Consolidate Python dependencies and introduce a real CI workflow.
3. Remove generated/local artifacts after checking what they contain.
4. Add a run log and screenshot from a reproducible test session.

For more reproducible examples, see [FluxPilot](https://github.com/Esoham/fluxpilot-automation), [SentinelWatch](https://github.com/Esoham/SentinelWatch-SOC-Lab) and [ChangeGuard MFG](https://github.com/Esoham/ChangeGuard_MFG_SUBMIT_READY_FLAT-).

*Retained as an earlier learning project; not included among pinned showcase recommendations.*
