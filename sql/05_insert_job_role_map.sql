-- Map jobs to roles by title keywords (run after 03_insert_staging_to_clean, 04_insert_lookup_levels_roles)

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'Backend'
WHERE lower(j.title) LIKE '%backend%'
   OR lower(j.title) LIKE '%back-end%'
   OR lower(j.title) LIKE '%back end%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'Frontend'
WHERE lower(j.title) LIKE '%frontend%'
   OR lower(j.title) LIKE '%front-end%'
   OR lower(j.title) LIKE '%front end%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'Fullstack'
WHERE lower(j.title) LIKE '%fullstack%'
   OR lower(j.title) LIKE '%full-stack%'
   OR lower(j.title) LIKE '%full stack%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'Mobile'
WHERE lower(j.title) LIKE '%android%'
   OR lower(j.title) LIKE '%ios%'
   OR lower(j.title) LIKE '%mobile%'
   OR lower(j.title) LIKE '%flutter%'
   OR lower(j.title) LIKE '%react native%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'Game'
WHERE lower(j.title) LIKE '%game%'
   OR lower(j.title) LIKE '%unity%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'QA'
WHERE lower(j.title) LIKE '%qa%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'QC'
WHERE lower(j.title) LIKE '%qc%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'DevOps'
WHERE lower(j.title) LIKE '%devops%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'SRE'
WHERE lower(j.title) LIKE '%sre%'
   OR lower(j.title) LIKE '%site reliability%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'Data Engineer'
WHERE lower(j.title) LIKE '%data engineer%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'Data Analyst'
WHERE lower(j.title) LIKE '%data analyst%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'Data Scientist'
WHERE lower(j.title) LIKE '%data scientist%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'AI'
WHERE j.title LIKE '%AI%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'Security'
WHERE lower(j.title) LIKE '%security%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'Cloud'
WHERE lower(j.title) LIKE '%cloud%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'System'
WHERE lower(j.title) LIKE '%system engineer%'
   OR lower(j.title) LIKE '%system admin%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'DBA'
WHERE lower(j.title) LIKE '%dba%'
   OR lower(j.title) LIKE '%database administrator%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'Architect'
WHERE lower(j.title) LIKE '%architect%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'Product'
WHERE lower(j.title) LIKE '%product manager%'
   OR lower(j.title) LIKE '%product owner%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'Software'
WHERE lower(j.title) LIKE '%software%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'Consultant'
WHERE lower(j.title) LIKE '%consultant%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'Business Analyst'
WHERE lower(j.title) LIKE '%business analyst%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'Designer'
WHERE lower(j.title) LIKE '%designer%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'Animator'
WHERE lower(j.title) LIKE '%animator%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'Blockchain'
WHERE lower(j.title) LIKE '%blockchain%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'Embedded'
WHERE lower(j.title) LIKE '%embedded%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'BrSE'
WHERE lower(j.title) LIKE '%brse%'
   OR lower(j.title) LIKE '%bridge software engineer%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'Manager'
WHERE lower(j.title) LIKE '%manager%'
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_role_map (job_id, role_id)
SELECT j.id, r.id
FROM clean.jobs j
JOIN clean.job_roles r ON r.name = 'Other'
WHERE j.id NOT IN (
    SELECT job_id FROM clean.job_role_map
)
ON CONFLICT DO NOTHING;
