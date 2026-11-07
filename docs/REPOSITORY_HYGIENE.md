# Repository hygiene and restoration

This QA portfolio contains FarmFresh, CommerceQA, automated UI and API testing, AI grading fixtures, and GitHub Actions.

## Why this cleanup exists
Historical commits accidentally tracked a Python virtual environment (venv/), compiled Python cache (__pycache__/), and local coverage binary (.coverage). These are reproducible generated artifacts, not source code. This change untracks only these root-level paths and extends .gitignore to prevent recurrence.

## What stays
Source code, tests, workflows, app templates, screenshots, relevant test evidence, READMEs, dependency manifests, and all previous Git commits remain available. Historical snapshots can be recovered by checking out the earlier commits.

## What this does not prove
This is **not** full Git history rewriting or credential purging. It does not establish that older commits are free of secrets. If any secret is ever discovered, rotate it and carry out a dedicated sensitive-history removal.

## Rebuild locally
```bash
python -m venv .venv
# Activate .venv for your platform
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
python -m pytest -q
```

The GitHub Actions workflow is the test acceptance gate for this cleanup.
