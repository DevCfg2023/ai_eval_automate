# ai_eval_automate
## LLM Guard: Universal AI Evaluation & Guardrail Framework
- LLM Guard is a production-grade Python package designed to bring Accountability, Transparency, and Safety to Generative AI processes.
- It provides a unified interface to measure model quality, detect performance drift, and enforce real-time security guardrails.
- It provides automated performance benchmarking, active safety guardrails, and historical drift monitoring to ensure AI accountability and reliability
---
## The Framework Architecture
### The framework is built on three core pillars to ensure AI reliability:
- Performance Verification: 
  Measuring Accuracy, BLEU, and F1 scores against "Ground Truth" data.
- Safety & Ethical AI: 
   Real-time toxicity detection and bias mitigation.
- Operational Monitoring: 
  Tracking latency, cost, and semantic drift over time.
  Drift Monitoring to identify if model quality degrades over time (Semantic or Output Drift).
---
Project Structure
```plaintext
ai_eval_automate/
├── .github/workflows/   # CI/CD automation (GitHub Actions)
├── src/
│   └── llm_guard/       # Core package source code
│       ├── engine.py    # Main evaluation orchestrator
│       ├── metrics.py   # Performance & Safety scoring logic
│       ├── guardrails.py # Active output filtering
│       └── monitor.py   # Historical drift detection
├── tests/               # Unit tests (Pytest)
├── main.py              # CLI entry point for developers
├── dashboard.py         # Streamlit web visualization
├── setup.py             # Package installation script
└── requirements.txt     # External dependencies
```
---
## Quick Start
1.Installation
You can install the framework as a local package for development:
```bash
# Clone the repository
git clone https://
cd ai_eval_automate
# Install in editable mode
pip install -e .
```
2.Run the Evaluation Pipeline
```bash
python main.py
```
3.Launch the Visualization Dashboard
```bash
streamlit run dashboard.py
```
---
## Usage
1.Automated Evaluation
Use the ProcessEvaluator to grade your model's outputs against a benchmark.

```python
from src.llm_guard import ProcessEvaluator

# Define predictions and ground truth
preds = ["The capital of France is Paris."]
truth = ["The capital of France is Paris."]

evaluator = ProcessEvaluator()
report = evaluator.evaluate(predictions=preds, references=truth)
```
2.Real-time Safety Guardrails
Intercept toxic or harmful content before it reaches your users.

```python
from src.llm_guard import GuardrailEngine

guard = GuardrailEngine(toxicity_threshold=0.4)
raw_output = "Some potentially harmful AI generation..."

# Returns safe fallback if toxicity is detected
safe_output = guard.validate_output(raw_output)
print(safe_output)
```
3.Visual Dashboard
Launch the Streamlit monitoring suite to track performance trends.
```bash
streamlit run dashboard.py
```
---

## Key Components
### Security & Adversarial Testing
The package includes a built-in "Red-Teaming" suite to test for prompt injections and jailbreaks. It automatically attempts to bypass your model's safety layers to ensure the GuardrailEngine is functioning correctly.

1.Active Guardrails
The GuardrailEngine acts as a security layer between the AI and the end-user. It evaluates outputs for toxicity and blocks responses that violate safety thresholds.

2.Drift Monitoring
Every evaluation is stored in history.json. The DriftMonitor compares current scores to historical averages and triggers alerts if performance drops by more than 10%.

3.Adversarial Testing
The framework includes a "Red Teaming" suite in main.py that simulates prompt injection attacks to verify that guardrails cannot be bypassed by malicious users.

---

## CI/CD Automation
- The included .github/workflows/eval_pipeline.yml ensures that your model is evaluated on every push. If the Safety Score or Accuracy falls below your defined thresholds, the build is automatically blocked.
- This project is pre-configured with GitHub Actions. On every push to main:
   A virtual environment is provisioned.
   The llm_guard package is installed.
   pytest runs the security and accuracy test suite.
   If safety or performance benchmarks are not met, the build fails, ensuring only high-quality models reach production.
---

## Package Components
- ProcessEvaluator: The main engine for batch evaluation.
- GuardrailEngine: Real-time safety filter.
- DriftMonitor: Tracks historical performance to detect "Model Decay."
- ToxicityMetric: Unbiased toxicity classifier based on Toxic-BERT.

---

## Smart Model Selection
- This framework allows you to perform A/B Testing and Comparative Evaluation across different LLM providers. By running the same "Golden Dataset" through multiple models, you can generate a side-by-side comparison.
- Comparative Analysis Example
- You can use the ProcessEvaluator to compare two models:

| Metric       | Model A (GPT-4) | Model B (Llama-3) | Winner   |
|-------------|----------------|------------------|----------|
| Accuracy    | 92%            | 88%              | Model A  |
| Latency     | 1.2s           | 0.4s             | Model B  |
| Safety Score| 0.98           | 0.95             | Model A  |
| Cost        | High           | Low              | Model B  |

---
## How to use for Model Selection:
- Run the suite for each model candidate.
- Analyze the Dashboard: Use the "Metric Distribution" chart to see which model hits your specific performance thresholds.
- Optimize for ROI: Choose the model that provides the highest accuracy while staying within your latency and budget constraints.
#### Evaluation Metrics

| Metric     | Purpose                                | Type        |
|------------|----------------------------------------|------------|
| Accuracy   | Measures correctness of responses      | Performance |
| Precision  | % of correct predicted answers         | Performance |
| Recall     | Coverage of relevant answers           | Performance |
| F1 Score   | Balance between precision & recall     | Performance |
| BLEU       | Text similarity (translation tasks)    | Language    |
| ROUGE      | Summarization quality                  | Language    |
| Perplexity | Language prediction confidence         | Language    |
| Latency    | Response speed                         | System      |
| Toxicity   | Harmful or biased content detection    | Safety      |

---

## Contributing
- Contributions are welcome! If you'd like to add new metrics (like ROUGE or BLEU) or improve the guardrail logic:
  <li>Fork the repo.</li>
  <li>Create your feature branch (git checkout -b feature/AmazingFeature).</li>
  <li>Commit your changes.</li>
  <li>Push to the branch.</li>
  <li>Open a Pull Request.</li>

---
