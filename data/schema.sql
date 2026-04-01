# Create the needed database
Create Database pc_diagnostics;

# Use the database you just created
USE pc_diagnostics;

# Create necessary tables
CREATE TABLE diagnostic_run (
    id INT AUTO_INCREMENT PRIMARY KEY,
    machine_name VARCHAR(255),
    os VARCHAR(100),
    start_dt DATETIME DEFAULT CURRENT_TIMESTAMP,
    end_dt DATETIME,
    duration_seconds INT,
    total_issues INT,
    severity_score INT,
    risk_level VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE scan_type (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE
);

CREATE TABLE issues (
    id INT AUTO_INCREMENT PRIMARY KEY,
    run_id INT NOT NULL,
	scan_type_id INT NOT NULL,
	type VARCHAR(255) NOT NULL,
	severity VARCHAR(50) NOT NULL,
    process VARCHAR(255),
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (run_id) REFERENCES diagnostic_run(id) ON DELETE CASCADE,
	FOREIGN KEY (scan_type_id) REFERENCES scan_type(id) ON DELETE RESTRICT
);

CREATE TABLE recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    issue_id INT NOT NULL,
    recommendation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE
);

# Create indexes for faster querying time
CREATE INDEX idx_risk_level ON diagnostic_run(risk_level);
CREATE INDEX idx_run_id ON issues(run_id);
CREATE INDEX idx_scan_type ON issues(scan_type_id);
CREATE INDEX idx_run_scan_type ON issues(run_id, scan_type_id);
CREATE INDEX idx_severity ON issues(severity);
CREATE INDEX idx_issue_id ON recommendations(issue_id);

# Insert scan type values into table scan_type
INSERT INTO scan_type (name) VALUES
('process'),
('system'),
('startup');