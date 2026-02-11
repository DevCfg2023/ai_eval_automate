import time
import pandas as pd
from typing import List, Dict, Any, Protocol
from dataclasses import dataclass
from enum import Enum
from detoxify import Detoxify
import numpy as np


# --- 1. Data Structures for Readability ---

class MetricStatus(Enum):
    EXCELLENT = "✅ Excellent"
    GOOD = "🟡 Good"
    FAIL = "❌ Critical"


@dataclass
class EvaluationReport:
    metric: str
    score: float
    benchmark: str
    status: str


# --- 2. Metric Interface (The Strategy) ---

class EvaluationMetric(Protocol):
    """Interface for all evaluation metrics."""

    def calculate(self, predictions: List[str], references: List[str]) -> float:
        ...


# --- 3. Concrete Metric Implementations ---

class AccuracyMetric:
    def calculate(self, predictions: List[str], references: List[str]) -> float:
        matches = sum(1 for p, r in zip(predictions, references) if p.strip().lower() == r.strip().lower())
        return matches / len(references) if references else 0.0


class BLEUMetric:
    """Simplified BLEU logic (Simulating 'evaluate' library)"""

    def calculate(self, predictions: List[str], references: List[str]) -> float:
        # In production: return evaluate.load("bleu").compute(...)
        # Simplified: Check word overlap percentage
        score_sum = 0
        for p, r in zip(predictions, references):
            p_set, r_set = set(p.split()), set(r.split())
            score_sum += len(p_set & r_set) / len(r_set) if r_set else 0
        return score_sum / len(predictions)


class LatencyMetric:
    def calculate(self, start_time: float, end_time: float) -> float:
        return end_time - start_time


class ToxicityMetric:
    def __init__(self, model_type: str = 'original'):
        """
        model_type options: 'original', 'unbiased', 'multilingual'
        'unbiased' is great for reducing false positives on identity terms.
        """
        # This will download the pre-trained weights on first run (~400MB)
        self.model = Detoxify(model_type)

    def calculate(self, predictions: List[str], references: List[str] = None) -> float:
        """
        Calculates the average toxicity across a batch of outputs.
        Note: Toxicity is a 'reference-less' metric (we don't need ground truth).
        """
        if not predictions:
            return 0.0

        # Predict returns a dict of scores for each category
        results = self.model.predict(predictions)

        # We focus on the 'toxicity' key, but could also check 'identity_hate'
        avg_toxicity = np.mean(results['toxicity'])

        # We return (1 - toxicity) so that a 'Higher Score' always means 'Better'
        # to match our dashboard logic where 1.0 is the goal.
        return 1.0 - float(avg_toxicity)