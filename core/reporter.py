# core/reporter.py
import pandas as pd
from datetime import datetime

def generate_report(issues):
    df = pd.DataFrame(issues)
    filename = f"scan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False)
    return filename