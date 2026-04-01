# data/db.py
import mysql.connector
import os
import socket
from dotenv import load_dotenv
from datetime import datetime
from core.ai_recommender import generate_recommendations

load_dotenv()

def connect():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def create_diagnostic_run():
    conn = connect()
    cursor = conn.cursor()

    machine_name = socket.gethostname()
    start_dt = datetime.now()

    cursor.execute("""
        INSERT INTO diagnostic_run (machine_name, start_dt)
        VALUES (%s, %s)
    """, (machine_name, start_dt))

    run_id = cursor.lastrowid

    conn.commit()
    cursor.close()
    conn.close()

    return run_id, start_dt

def insert_scan_results(run_id, issues):
    conn = connect()
    cursor = conn.cursor()

    scan_type_map = get_scan_type_map()

    issue_ids = []

    for issue in issues:
        try:
            scan_type_id = scan_type_map[issue['scan_type']]
        except KeyError:
            # fallback (log + skip OR assign default)
            print(f"Unknown scan_type: {issue.get('scan_type')}")
            scan_type_id = -1
        cursor.execute("""
                    INSERT INTO issues (run_id, scan_type_id, type, severity, process, details)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
            run_id,
            scan_type_id,
            issue['type'],
            issue['severity'],
            issue.get('process', ''),
            issue['details']
        ))
        issue_ids.append(cursor.lastrowid)

    conn.commit()
    cursor.close()
    conn.close()

    return issue_ids

def finalize_diagnostic_run(run_id, start_dt, issues, severity_score, risk_level):
    from datetime import datetime

    conn = connect()
    cursor = conn.cursor()

    end_dt = datetime.now()
    duration = int((end_dt - start_dt).total_seconds())
    total_issues = len(issues)

    cursor.execute("""
        UPDATE diagnostic_run
        SET end_dt = %s,
            duration_seconds = %s,
            total_issues = %s,
            severity_score = %s,
            risk_level = %s
        WHERE id = %s
    """, (
        end_dt,
        duration,
        total_issues,
        severity_score,
        risk_level,
        run_id
    ))

    conn.commit()
    cursor.close()
    conn.close()

def get_scan_type_map():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM scan_type")
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return {name: id for (id, name) in results}

def insert_recommendations(issue_ids, issues):
    conn = connect()
    cursor = conn.cursor()

    for issue_id, issue in zip(issue_ids, issues):
        rec = generate_recommendations(issue)

        cursor.execute("""
            INSERT INTO recommendations (issue_id, recommendation)
            VALUES (%s, %s)
        """, (issue_id, rec))

    conn.commit()
    cursor.close()
    conn.close()