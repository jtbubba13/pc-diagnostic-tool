from scanners.process_scanner import run_process_scan
from scanners.system_scanner import run_system_scan
from scanners.startup_scanner import run_startup_scan
from core.rules_engine import evaluate_processes, evaluate_system, calculate_risk_score, classify_risk, evaluate_startup
from core.reporter import generate_report
from data.db import create_diagnostic_run, insert_scan_results, finalize_diagnostic_run, insert_recommendations

def main():
    # Update to logging
    print("Starting diagnostic run...")

    # Step 1: Start run
    run_id, start_dt = create_diagnostic_run()

    # Step 2: Run all scans
    # Process Scanner
    process_data = run_process_scan()
    issues = evaluate_processes(process_data)

    # System Scanner
    system_data = run_system_scan()
    issues.extend(evaluate_system(system_data))

    # Startup Scanner
    startup_data = run_startup_scan()
    issues.extend(evaluate_startup(startup_data))

    # Update to logging
    print('Run Id = ', run_id, 'Issues = ', issues)

    # Step 3: Insert issues into the database
    issue_ids = insert_scan_results(run_id, issues)

    # Step 4: Calculate the risk score
    severity_score = calculate_risk_score(issues)
    risk_level = classify_risk(severity_score)

    # Step 5: Get AI recommendations
    # insert_recommendations(issue_ids, issues)

    # Step 6: Update database with end time, severity score, and risk level information
    finalize_diagnostic_run(run_id, start_dt, issues, severity_score, risk_level)

    # Update to logging
    print(f"Run complete. Risk Level: {risk_level}")

    # Step 7: Generate Report
    report_file = generate_report(issues)
    # Update to logging
    print(f"Report saved to {report_file}")

if __name__ == "__main__":
    main()