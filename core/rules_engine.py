import core.constants as const

# core/rules_engine.py
def evaluate_processes(df):
    issues = []
    scan_type = const.PROCESS

    for _, row in df.iterrows():
        if row['cpu'] > 80:
            issues.append({
                "type": "High CPU Usage",
                "process": row['name'],
                "severity": "Medium",
                "details": f"CPU usage at {row['cpu']}%",
                "scan_type": scan_type
            })

        if row['path'] and "AppData" in row['path']:
            issues.append({
                "type": "Suspicious Location",
                "process": row['name'],
                "severity": "High",
                "details": f"Running from {row['path']}",
                "scan_type": scan_type
            })
    print(issues)
    return issues

def evaluate_system(system_data):
    issues = []
    scan_type = const.SYSTEM

    if system_data["memory"]["memory_usage_percent"] > 85:
        issues.append({
            "type": "High Memory Usage",
            "severity": "Medium",
            "details": f"Memory usage at {system_data['memory']['memory_usage_percent']}%",
            "scan_type": scan_type
        })

    for disk in system_data["disk"]:
        if disk["usage_percent"] > 90:
            issues.append({
                "type": "Low Disk Space",
                "severity": "High",
                "details": f"{disk['mountpoint']} at {disk['usage_percent']}%",
                "scan_type": scan_type
            })
    print(issues)
    return issues

def evaluate_startup(startup_items):
    issues = []
    scan_type = const.STARTUP

    for item in startup_items:
        name = item.get("name", "")
        command = item.get("command", "")

        if "AppData" in command:
            issues.append({
                "type": "Suspicious Startup Location",
                "severity": "High",
                "details": f"{name} runs from {command}",
                "scan_type": scan_type
            })

        if not command:
            issues.append({
                "type": "Empty Startup Entry",
                "severity": "Low",
                "details": f"{name} has no command",
                "scan_type": scan_type
            })

        if ".exe" not in command:
            issues.append({
                "type": "Unusual Startup Command",
                "severity": "Medium",
                "details": f"{name} uses non-standard command: {command}",
                "scan_type": scan_type
            })
    print(issues)
    return issues

def calculate_risk_score(issues):
    total_score = 0

    for issue in issues:
        severity = issue.get("severity", "Low")
        total_score += SEVERITY_SCORE.get(severity, 1)

    return total_score

def classify_risk(score):
    if score < 5:
        return "Healthy"
    elif score < 10:
        return "Moderate Risk"
    else:
        return "High Risk"

SEVERITY_SCORE = {
    "Low": 1,
    "Medium": 2,
    "High": 3
}


