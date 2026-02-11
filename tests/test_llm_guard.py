import pytest
from llm_guard import GuardrailEngine, AccuracyMetric, ToxicityMetric


# 1. Test the Guardrail Logic
def test_guardrail_blocking():
    # Setup engine with a strict threshold
    guard = GuardrailEngine(toxicity_threshold=0.1)

    toxic_input = "I am going to attack and insult everyone!"
    safe_input = "The weather is quite lovely today."

    # Assert toxic input is replaced by fallback
    assert guard.validate_output(toxic_input) == guard.safe_fallback
    # Assert safe input passes through
    assert guard.validate_output(safe_input) == safe_input


# 2. Test the Accuracy Metric
def test_accuracy_calculation():
    metric = AccuracyMetric()
    preds = ["Paris", "Berlin", "London"]
    truth = ["Paris", "Berlin", "Madrid"]

    score = metric.calculate(preds, truth)
    # 2 out of 3 are correct = 0.666...
    assert pytest.approx(score, 0.01) == 0.66


# 3. Test Toxicity Scoring (Non-blocking)
def test_toxicity_score_range():
    metric = ToxicityMetric()
    # Testing that the score is a float between 0 and 1
    score = metric.calculate(["This is a neutral sentence."])
    assert 0.0 <= score <= 1.0