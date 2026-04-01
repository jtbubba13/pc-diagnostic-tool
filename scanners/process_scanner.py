# scanners/process_scanner.py
import psutil
import pandas as pd

def run_process_scan():
    process_data = []

    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'exe']):
        try:
            info = proc.info

            process_data.append({
                "pid": info['pid'],
                "name": info['name'],
                "user": info['username'],
                "cpu": info['cpu_percent'],
                "memory": info['memory_percent'],
                "path": info['exe']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    df = pd.DataFrame(process_data)
    return df