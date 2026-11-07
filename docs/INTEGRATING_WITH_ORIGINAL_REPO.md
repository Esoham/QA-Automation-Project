# Integrating CommerceQA into `Esoham/QA-Automation-Project`

This portfolio upgrade is designed to be copied into the **root** of the existing `QA-Automation-Project` GitHub repository, preferably on a new branch and reviewed via a pull request.

## What changes

- Adds a clean standalone product/quote API under `commerceqa/`.
- Adds `tests/` with reliable Playwright and API regression tests.
- Adds `evals/` with synthetic AI-response evaluation cases and graders.
- Adds a GitHub Actions workflow, install manifest, and clearly marked verification evidence.
- Does **not** delete historical FarmFresh files; the new root `pytest.ini` restricts discovery to the verified `tests/` folder rather than broken legacy scripts.

## Suggested Git workflow (from a checkout of your original repository)

```bash
git checkout -b feat/commerceqa-automation-lab
# Extract CommerceQA_QA_Automation_Portfolio_Upgrade.zip into this checkout.
# Inspect git status before staging anything.
git add commerceqa tests evals docs evidence pytest.ini requirements-dev.txt .github/workflows/commerceqa-ci.yml .gitignore README.md
git commit -m "Add verified Playwright API and AI evaluation QA lab"
git push -u origin feat/commerceqa-automation-lab
```

**History cleanup recommended but not performed by this zip:** The original repository tracks `venv/`, caches, and coverage/build files. After inspecting them for secrets and ensuring no evidence needs preserving, use a separate cleanup commit to stop tracking generated artifacts (`git rm -r --cached ...`), not `rm -rf` on your working machine. Never commit actual environment secrets or customer data.

## One README decision

The archive's root `README.md` describes the new lab. Keep a link to the archived FarmFresh project in that README if you want to preserve the learning-project history visibly.

## Verification requirement

The local test evidence used in-process Chromium API routing because this runtime blocked normal navigation. Once the branch is uploaded, check the GitHub Actions job for the **normal** localhost browser run before calling the full project CI-verified. Review its JUnit report and traces if failures occur.
