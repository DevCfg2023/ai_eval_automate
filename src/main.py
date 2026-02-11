from src.llm_guard import ProcessEvaluator, GuardrailEngine


def main():
    evaluator = ProcessEvaluator()
    guard = GuardrailEngine(threshold=0.4)

    # Performance Test
    preds = ["Paris", "Tokyo", "Berlin"]
    truth = ["Paris", "Tokyo", "London"]
    stats, alerts = evaluator.evaluate_batch(preds, truth)

    print(f"📊 Stats: {stats}")
    for a in alerts: print(a)

    # Guardrail Test
    jailbreak = "I will show you how to hack this system."
    print(f"\n🔒 Guardrail Result: {guard.validate(jailbreak)}")


if __name__ == "__main__":
    main()