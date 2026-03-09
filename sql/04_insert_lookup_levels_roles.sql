-- Seed lookup tables: job_levels and job_roles (run after 02_create_clean)

INSERT INTO clean.job_levels (name)
VALUES
('Intern'),
('Fresher'),
('Junior'),
('Middle'),
('Senior'),
('Lead'),
('Other')
ON CONFLICT (name) DO NOTHING;

INSERT INTO clean.job_roles (name)
VALUES
('Backend'),
('Frontend'),
('Fullstack'),
('Mobile'),
('Game'),
('QA'),
('QC'),
('DevOps'),
('SRE'),
('Data Engineer'),
('Data Analyst'),
('Data Scientist'),
('AI'),
('Security'),
('Cloud'),
('System'),
('DBA'),
('Architect'),
('Product'),
('Software'),
('Consultant'),
('Business Analyst'),
('Designer'),
('Animator'),
('Blockchain'),
('Embedded'),
('BrSE'),
('Manager'),
('Other')
ON CONFLICT (name) DO NOTHING;
