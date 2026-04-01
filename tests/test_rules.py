# tests/test_rules.py
from core.rules_engine import evaluate_processes
import pandas as pd

def test_high_cpu():
    df = pd.DataFrame([{"name": "test", "cpu": 90, "path": "C:\\test.exe"}])
    issues = evaluate_processes(df)
    assert len(issues) > 0