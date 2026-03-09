-- Insert from staging into clean (run after 01_create_staging, 02_create_clean)

INSERT INTO clean.companies (name)
SELECT DISTINCT company
FROM staging.companies
ON CONFLICT (name) DO NOTHING;

INSERT INTO clean.skills (name)
SELECT DISTINCT skill
FROM staging.skills
ON CONFLICT (name) DO NOTHING;

INSERT INTO clean.locations (name)
SELECT DISTINCT location
FROM staging.locations
ON CONFLICT (name) DO NOTHING;

INSERT INTO clean.jobs (title, salary, url, company_id)
SELECT
    j.title,
    j.salary,
    j.url,
    c.id
FROM staging.jobs j
LEFT JOIN clean.companies c
    ON j.company = c.name
ON CONFLICT (url) DO NOTHING;

INSERT INTO clean.job_skills (job_id, skill_id)
SELECT
    j.id,
    sk.id
FROM staging.job_skills js
JOIN clean.jobs j ON js.url = j.url
JOIN clean.skills sk ON js.skill = sk.name
ON CONFLICT DO NOTHING;

INSERT INTO clean.job_locations (job_id, location_id)
SELECT
    j.id,
    l.id
FROM staging.job_locations jl
JOIN clean.jobs j ON jl.url = j.url
JOIN clean.locations l ON jl.location = l.name
ON CONFLICT DO NOTHING;
