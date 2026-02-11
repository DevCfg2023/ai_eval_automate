import json
import os
from typing import Dict


class DriftMonitor:
    def __init__(self, storage_path: str = "data/history.json"):
        self.storage_path = storage_path
        self.baseline = self._load_history()

    def _load_history(self) -> Dict:
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return {}

    def check_drift(self, current_metrics: Dict[str, float], sensitivity: float = 0.1):
        """
        Compares current scores to the historical average.
        sensitivity: 0.1 means a 10% drop triggers an alert.
        """
        drift_alerts = []

        for metric, current_val in current_metrics.items():
            if metric in self.baseline:
                previous_val = self.baseline[metric]
                # Calculate percentage change
                change = (current_val - previous_val) / previous_val if previous_val != 0 else 0

                if change < -sensitivity:
                    drift_alerts.append(
                        f"⚠️ DRIFT DETECTED: {metric} dropped by {abs(change):.1%}"
                    )

        # Update baseline with current run (moving average logic)
        self._update_history(current_metrics)
        return drift_alerts

    def _update_history(self, new_metrics: Dict):
        # In a real app, you'd use a moving average; here we just save the latest
        with open(self.storage_path, 'w') as f:
            json.dump(new_metrics, f)