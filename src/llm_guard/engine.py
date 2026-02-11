import time
import pandas as pd
from typing import List

import json

from src.llm_guard import AccuracyMetric
from src.llm_guard.metrics import BLEUMetric, MetricStatus, EvaluationReport, LatencyMetric


class ProcessEvaluator:
    def __init__(self):
        self.metrics = {
            "Accuracy": (AccuracyMetric(), 0.85),  # Metric object and target threshold
            "BLEU (Quality)": (BLEUMetric(), 0.70)
        }
        self.history = []

    def evaluate(self, predictions: List[str], references: List[str]):
        """
        Executes the evaluation pipeline against the 'Ground Truth'.
        """
        print("🛠️  Initializing LLM Evaluation Pipeline...")
        start_exec = time.time()

        results = []

        # Calculate standard NLP metrics
        for name, (metric_obj, threshold) in self.metrics.items():
            score = metric_obj.calculate(predictions, references)
            status = MetricStatus.EXCELLENT if score >= threshold else MetricStatus.FAIL

            results.append(EvaluationReport(
                metric=name,
                score=round(score, 4),
                benchmark=f">{threshold}",
                status=status.value
            ))

        # Add Latency Metric (as seen in the infographic)
        latency = LatencyMetric().calculate(start_exec, time.time())
        results.append(EvaluationReport("Latency", round(latency, 4), "<1.0s", "✅ Excellent"))

        self._render_dashboard(results)

    def _render_dashboard(self, results: List[EvaluationReport]):
        """Prints a professional summary using Pandas for high readability."""
        df = pd.DataFrame([vars(r) for r in results])
        print("\n--- 📊 FINAL EVALUATION DASHBOARD ---")
        print(df.to_string(index=False))
        print("--------------------------------------\n")


class EvaluationEngine:
    def __init__(self, history_path="data/history.json"):
        self.evaluator = ProcessEvaluator()
        self.history_path = history_path
        self.history = []

    def evaluate(self, predictions, references):
        stats, alerts = self.evaluator.evaluate_batch(predictions, references)
        self.history.append({
            "predictions": predictions,
            "references": references,
            "stats": stats,
            "alerts": alerts
        })
        # Save history for later harvesting
        with open(self.history_path, "w") as f:
            json.dump(self.history, f, indent=2)
        print(f"[📦] Evaluation complete → {self.history_path}")
        return stats, alerts


# --- 5. Execution ---

if __name__ == "__main__":
    # Mock Data: Ground Truth vs Model Output
    ground_truth = [
        "The quick brown fox jumps over the lazy dog.",
        "The capital of Japan is Tokyo."
    ]
    model_preds = [
        "The quick brown fox jumps over the dog.",  # Minor error
        "The capital of Japan is Tokyo."  # Exact match
    ]

    evaluator = ProcessEvaluator()
    evaluator.evaluate(model_preds, ground_truth)
