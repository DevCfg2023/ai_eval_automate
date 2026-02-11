# from src.llm_guard import ProcessEvaluator, GuardrailEngine
from src.llm_guard.engine import EvaluationEngine
from src.llm_guard.guardrails import GuardrailWrapper
from src.utils.data_prep import harvest_failures
from src.utils.train import fine_tune


# def main():
#     evaluator = ProcessEvaluator()
#     guard = GuardrailEngine(threshold=0.4)
#
#     # Performance Test
#     preds = ["Paris", "Tokyo", "Berlin"]
#     truth = ["Paris", "Tokyo", "London"]
#     stats, alerts = evaluator.evaluate_batch(preds, truth)
#
#     print(f"📊 Stats: {stats}")
#     for a in alerts: print(a)
#
#     # Guardrail Test
#     jailbreak = "I will show you how to hack this system."
#     print(f"\n🔒 Guardrail Result: {guard.validate(jailbreak)}")


def main():
    # Initialize evaluators
    evaluator = EvaluationEngine()
    guard = GuardrailWrapper(threshold=0.4)

    # Performance Test
    preds = ["Paris", "Tokyo", "Berlin"]
    truth = ["Paris", "Tokyo", "London"]

    stats, alerts = evaluator.evaluate(preds, truth)
    print(f"📊 Stats: {stats}")
    for a in alerts:
        print(a)

    # Guardrail Test
    jailbreak = "I will show you how to hack this system."
    print(f"\n🔒 Guardrail Result: {guard.validate_input(jailbreak)}")

    # Harvest failures for fine-tuning
    harvest_failures(threshold=0.85)

    # Fine-tune model on harvested failures
    fine_tune()


if __name__ == "__main__":
    main()
