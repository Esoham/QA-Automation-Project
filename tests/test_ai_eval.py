"""Test the evaluator, including whether it rejects deliberately wrong model outputs."""
import json
from pathlib import Path

from evals.grade import evaluate

HERE = Path(__file__).resolve().parents[1] / "evals"


def fixtures():
    return json.loads((HERE / "golden_cases.json").read_text()), json.loads((HERE / "sample_model_outputs.json").read_text())


def test_known_good_synthetic_responses_are_graded_as_expected():
    gold, candidates = fixtures()
    report = evaluate(gold, candidates)
    assert report["total"] == 8
    assert report["passed"] == 8


def test_evaluator_catches_hallucinated_sku_and_wrong_inventory():
    gold, responses = fixtures()
    responses["exact-bolt"]["recommended_skus"] = ["BOLT-FAKE"]
    responses["exact-bolt"]["product_claims"][0]["value"] = 99999
    result = evaluate(gold, responses)
    assert result["passed"] == 7
    errors = " ".join(result["cases"][0]["errors"])
    assert "Invented" in errors and "Incorrect" in errors


def test_evaluator_catches_bad_refusal_and_prompt_injection_leak():
    gold, responses = fixtures()
    responses["prompt-injection"]["refused"] = False
    responses["prompt-injection"]["answer"] = "api_key=bad_value"
    result = evaluate(gold, responses)
    assert result["passed"] == 7
    errors = " ".join(result["cases"][-1]["errors"])
    assert "refusal" in errors and "secret" in errors


def test_evaluator_fails_on_missing_response():
    gold, responses = fixtures()
    del responses["tape"]
    assert evaluate(gold, responses)["passed"] == 7
